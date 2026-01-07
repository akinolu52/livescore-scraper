"""
Streamlit web application for LiveScore team game crawler.
"""

import streamlit as st
import pandas as pd
from io import StringIO
from scraper import get_team_games


def main():
    st.set_page_config(
        page_title="LiveScore Game Crawler",
        page_icon="⚽",
        layout="wide"
    )
    
    st.title("⚽ LiveScore Team Game Crawler")
    st.markdown("Fetch and download the last N games for any football team from LiveScore")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Team Information")
        
        team_name = st.text_input(
            "Team Name (URL format)",
            value="west-ham-united",
            help="Use the team name as it appears in LiveScore URLs (e.g., 'west-ham-united')"
        )
        
        team_id = st.text_input(
            "Team ID",
            value="252",
            help="Numeric team ID from LiveScore URL (e.g., 252 for West Ham)"
        )
        
        num_games = st.number_input(
            "Number of Games",
            min_value=1,
            max_value=50,
            value=10,
            help="Maximum number of recent games to fetch"
        )
        
        fetch_button = st.button("🔍 Fetch Games", type="primary", width="stretch")
        
        st.markdown("---")
        st.markdown("""
        ### How to find Team Info
        1. Visit [livescore.com](https://www.livescore.com)
        2. Search for your team
        3. Check the URL:\n
           `/team/west-ham-united/252/`
           - Team Name: `west-ham-united`
           - Team ID: `252`
        """)
    
    # Main content area
    if fetch_button:
        if not team_name or not team_id:
            st.error("Please provide both Team Name and Team ID")
            return
        
        try:
            with st.spinner(f"Fetching games for {team_name}..."):
                # Fetch games
                games = get_team_games(team_id, team_name, limit=num_games)
                
                if not games:
                    st.warning("No games found for this team")
                    return
                
                # Convert to DataFrame
                df = pd.DataFrame(games)
                
                # Display success message
                st.success(f"✅ Fetched {len(games)} game(s) for {team_name}")
                
                # Display data
                st.subheader("Games")
                st.dataframe(
                    df,
                    width="stretch",
                    hide_index=True
                )
                
                # CSV download
                csv_buffer = StringIO()
                df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()
                
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv_data,
                    file_name=f"{team_name}_games.csv",
                    mime="text/csv",
                    width="stretch",
                )
                
                # Store in session state for persistence
                st.session_state['last_df'] = df
                st.session_state['last_team'] = team_name
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Please check your team name and ID, or try again later.")
    
    # Show last fetched data if available
    elif 'last_df' in st.session_state:
        st.info(f"Showing last fetched data for: {st.session_state['last_team']}")
        st.dataframe(
            st.session_state['last_df'],
            width="stretch",
            hide_index=True
        )
        
        csv_buffer = StringIO()
        st.session_state['last_df'].to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 Download as CSV",
            data=csv_data,
            file_name=f"{st.session_state['last_team']}_games.csv",
            mime="text/csv",
            width="stretch",
        )
    else:
        # Welcome message
        st.info("👈 Enter team information in the sidebar and click 'Fetch Games' to get started!")
        
        # Example teams
        st.subheader("Example Teams")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **Premier League**
            - West Ham United: `west-ham-united` / `252`
            - Arsenal: `arsenal` / `675`
            - Liverpool: `liverpool` / `24`
            """)
        
        with col2:
            st.markdown("""
            **La Liga**
            - Real Madrid: `real-madrid` / `418`
            - Barcelona: `barcelona` / `421`
            """)
        
        with col3:
            st.markdown("""
            **Serie A**
            - Juventus: `juventus` / `506`
            - AC Milan: `ac-milan` / `511`
            """)


if __name__ == "__main__":
    main()
