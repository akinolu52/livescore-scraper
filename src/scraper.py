"""
LiveScore scraper module to fetch and parse team game data.
"""

import re
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, List
from datetime import datetime


class LiveScoreScraper:
    """Scraper for LiveScore team game data."""
    
    BASE_URL = "https://www.livescore.com"
    _cached_build_id: Optional[str] = None
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def extract_build_id(self) -> str:
        """
        Extract the Next.js build ID from LiveScore's homepage.
        The build ID is cached to minimize requests.
        
        Returns:
            str: The build ID
            
        Raises:
            Exception: If build ID cannot be extracted
        """
        if self._cached_build_id:
            return self._cached_build_id
        
        try:
            response = self.session.get(self.BASE_URL, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for Next.js build ID in script tags
            # Build ID is typically in _next/static/<BUILD_ID>/
            scripts = soup.find_all('script', src=True)
            for script in scripts:
                src = script.get('src', '')
                match = re.search(r'/_next/static/([^/]+)/', src)
                if match:
                    build_id = match.group(1)
                    if build_id and build_id != 'chunks':
                        LiveScoreScraper._cached_build_id = build_id
                        return build_id
            
            # Alternative: look for buildId in JSON
            for script in soup.find_all('script', id='__NEXT_DATA__'):
                text = script.string
                if text:
                    match = re.search(r'"buildId":"([^"]+)"', text)
                    if match:
                        build_id = match.group(1)
                        LiveScoreScraper._cached_build_id = build_id
                        return build_id
            
            raise Exception("Could not find Next.js build ID in page source")
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch LiveScore homepage: {e}")
    
    def fetch_team_games(
        self, 
        team_id: str, 
        team_name: str, 
        build_id: Optional[str] = None
    ) -> Dict:
        """
        Fetch raw game data for a team from LiveScore API.
        
        Args:
            team_id: The team's numeric ID
            team_name: The team's URL-friendly name (e.g., 'west-ham-united')
            build_id: Optional build ID. If not provided, it will be extracted automatically
            
        Returns:
            dict: Raw JSON response from LiveScore API
            
        Raises:
            Exception: If data cannot be fetched
        """
        if not build_id:
            build_id = self.extract_build_id()
        
        url = (
            f"{self.BASE_URL}/_next/data/{build_id}/en/football/team/"
            f"{team_name}/{team_id}/results.json"
        )
        
        params = {
            'sport': 'football',
            'teamName': team_name,
            'teamId': team_id
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch team data: {e}")
    
    def parse_games(self, data: Dict, limit: Optional[int] = None) -> List[Dict]:
        """
        Parse game data from LiveScore API response.
        
        Args:
            data: Raw JSON response from fetch_team_games
            limit: Optional limit on number of games to return
            
        Returns:
            list: List of parsed game dictionaries
        """
        games = []
        
        try:
            # Extract results from the API response
            initial_data = data.get('pageProps', {}).get('initialData', {})
            
            # The results.json endpoint has eventsByMatchType array with Events
            events_by_match_type = initial_data.get('eventsByMatchType', [])
            
            # Flatten all events from all match types
            for match_type_group in events_by_match_type:
                events = match_type_group.get('Events', [])
                comp_name = match_type_group.get('CompN', 'N/A')
                stage_name = match_type_group.get('Snm', 'N/A')
                
                for event in events:
                    if limit and len(games) >= limit:
                        return games
                    
                    # Parse date/time (Esd field)
                    date_str = event.get('Esd', '')
                    try:
                        date_obj = datetime.strptime(str(date_str), '%Y%m%d%H%M%S')
                        formatted_date = date_obj.strftime('%Y-%m-%d %H:%M')
                    except:
                        formatted_date = str(date_str)
                    
                    # Extract team names from T1 and T2 arrays
                    t1 = event.get('T1', [{}])[0]
                    t2 = event.get('T2', [{}])[0]
                    home_team = t1.get('Nm', 'N/A')
                    away_team = t2.get('Nm', 'N/A')
                    
                    # Extract score from Tr1 and Tr2
                    home_score = event.get('Tr1', '')
                    away_score = event.get('Tr2', '')
                    score = f"{home_score}-{away_score}" if home_score and away_score else "vs"
                    
                    # Status from Eps
                    status = event.get('Eps', 'N/A')
                    
                    # Build game dictionary
                    parsed_game = {
                        'Date': formatted_date,
                        'Home Team': home_team,
                        'Away Team': away_team,
                        'Score': score,
                        'Competition': comp_name,
                        'Stage': stage_name,
                        'Status': status,
                    }

                    games.append(parsed_game)
            
            return games
            
        except Exception as e:
            raise Exception(f"Failed to parse game data: {e}")


def get_team_games(team_id: str, team_name: str, limit: Optional[int] = None) -> List[Dict]:
    """
    Convenience function to fetch and parse team games in one call.
    
    Args:
        team_id: The team's numeric ID
        team_name: The team's URL-friendly name
        limit: Optional limit on number of games
        
    Returns:
        list: List of parsed game dictionaries
    """
    scraper = LiveScoreScraper()
    data = scraper.fetch_team_games(team_id, team_name)
    return scraper.parse_games(data, limit)
