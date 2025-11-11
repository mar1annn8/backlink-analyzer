import streamlit as st
import pandas as pd
from urllib.parse import urlparse

# Set page config for a wider layout
st.set_page_config(layout="wide")

def analyze_url(url):
    """
    Simulates the analysis of a single URL in Python with more specific rules.
    """
    try:
        # Use urlparse to reliably get the domain
        domain = urlparse(url).netloc.replace('www.', '')
    except Exception:
        domain = "" # Handle invalid URLs

    # Default values
    quality = 'Low'
    domain_authority = 'Very Low'
    link_type = 'Unknown'
    assessment = ''
    recommendation = ''
    action = 'Monitor' # Action is the single-word category

    # --- Updated Mock Analysis Logic (Python version) ---
    high_quality_domains = [
        'zillow.com', 'realtor.com', 'redfin.com', 'trulia.com',
        'gritdaily.com', 'forbes.com', 'wsj.com', 'nytimes.com',
        'luxuryhomemarketing.com', 'wcr.org'
    ]
    
    # Added more specific lists based on your examples
    spam_networks = ['spam-network-example.com', 'link-farm-domain.net']
    job_patterns = ['jobsapp', 'job-listing.com']
    spam_indicators = [
        'blogspot.com', 'wordpress.com', 'notifyninja.com', 
        'christmas-blog-spam.com'
    ]
    low_quality_patterns = ['bizlistings', 'visualvisitor']


    if any(d in domain for d in high_quality_domains):
        if 'zillow.com' in domain or 'realtor.com' in domain:
            quality = 'High'
            domain_authority = 'Very High'
            link_type = 'Agent Profile'
            assessment = 'Excellent - Major real estate platform with high authority'
            recommendation = 'Keep - Premium link'
            action = 'Maintain'
        elif 'gritdaily.com' in domain or 'forbes.com' in domain:
            quality = 'High'
            domain_authority = 'High'
            link_type = 'Editorial/Contextual'
            assessment = 'Excellent - Legitimate tech/business publication with editorial content' # Your example
            recommendation = 'Keep - High value link' # Your example
            action = 'Maintain'
        elif 'luxuryhomemarketing.com' in domain or 'wcr.org' in domain:
            quality = 'High'
            domain_authority = 'Medium-High'
            link_type = 'Professional Directory'
            assessment = 'Good - Industry-relevant professional organization'
            recommendation = 'Keep - Industry authority'
            action = 'Maintain'
    
    elif any(s in domain for s in spam_networks):
        quality = 'Very Low'
        domain_authority = 'Very Low'
        link_type = 'Spam Network'
        assessment = 'Poor - Part of spam blog network' # Your example
        recommendation = 'Disavow - Spam network' # Your example
        action = 'Disavow'

    elif any(s in domain for s in spam_indicators):
        quality = 'Very Low'
        domain_authority = 'Very Low'
            
        if 'blogspot.com' in domain:
            link_type = 'Spam Blog'
            assessment = 'Poor - Auto-generated spam blog with scraped content' # Your example
            recommendation = 'Disavow - Potential SEO harm' # Your example
            action = 'Disavow'
        elif 'notifyninja.com' in domain:
            link_type = 'Tool/Utility'
            assessment = 'Poor - Website monitoring tool with no SEO value' # Your example
            recommendation = 'Disavow - 9 duplicate links, zero value' # Your example
            action = 'Disavow'
        elif 'wordpress.com' in domain:
            link_type = 'Blog Post'
            quality = 'Low-Medium'
            assessment = 'Context-dependent - Could be legitimate charity/organization' # Your example
            recommendation = 'Review - Check relevance and context' # Your example
            action = 'Review'
        elif 'christmas-blog-spam.com' in domain:
            link_type = 'Spam Blog'
            assessment = 'Poor - Irrelevant spam blog (Christmas content)' # Your example
            recommendation = 'Disavow - Completely irrelevant' # Your example
            action = 'Disavow'

    elif any(p in domain for p in job_patterns):
        quality = 'Low'
        domain_authority = 'Very Low'
        link_type = 'Job Board'
        assessment = 'Poor - Low quality job/business directory' # Your example
        recommendation = 'Monitor - Minimal SEO value' # Your example
        action = 'Monitor'
    
    elif any(p in domain for p in low_quality_patterns):
        quality = 'Low'
        domain_authority = 'Very Low'
        link_type = 'Generic Directory'
        assessment = 'Poor - Low authority generic business directory' # Your example
        recommendation = 'Monitor - Minimal benefit, likely harmless' # Your example
        action = 'Monitor'
    
    elif 'chamber' in domain:
        quality = 'Medium-High'
        domain_authority = 'Medium'
        link_type = 'Local Directory'
        assessment = 'Good - Local chamber of commerce, geographically relevant'
        recommendation = 'Keep - Local SEO value'
        action = 'Maintain'
    
    elif 'homein' in domain or 'home' in domain or 'property' in url:
        quality = 'Low'
        domain_authority = 'Very Low'
        link_type = 'Property Site'
        assessment = 'Neutral - Single property listing site'
        recommendation = 'Monitor - Limited ongoing value'
        action = 'Monitor'
    
    elif 'adapt.io' in domain:
        quality = 'Low'
        domain_authority = 'Medium'
        link_type = 'Contact Database'
        assessment = 'Neutral - B2B contact database, limited SEO benefit'
        recommendation = 'Monitor - No action needed'
        action = 'Monitor'
    
    else:
        # --- UPDATED DEFAULT LOGIC ---
        # Default for unmatched links
        quality = 'Low'
        domain_authority = 'Low'
        link_type = 'General'
        assessment = 'Low - Unclassified link, minimal SEO benefit'
        recommendation = 'Monitor - Minimal benefit, likely harmless'
        action = 'Monitor'
    
    return {
        'Domain': domain,
        'Quality': quality,
        'Domain Authority': domain_authority,
        'Link Type': link_type,
        'Assessment': assessment,
        'Recommendation': recommendation,
        'Action': action,
        'URL': url
    }

def get_color_style(val):
    """
    Applies background color style based on quality.
    Uses light, readable colors.
    """
    val = str(val).lower()
    if 'high' in val:
        return 'background-color: #D6FFD6' # Light Green
    if 'medium' in val:
        return 'background-color: #FFFFD6' # Light Yellow
    if 'low' in val:
        return 'background-color: #FFD6D6' # Light Red
    return '' # Default

# --- Main App UI ---

# Initialize session state
if 'backlinks_df' not in st.session_state:
    st.session_state.backlinks_df = None
    st.session_state.input_urls = ""

st.title("Backlink Quality Analyzer")
st.write("Analyze the quality of your backlinks and get actionable recommendations")

# --- Input Screen ---
if st.session_state.backlinks_df is None:
    with st.container(border=True):
        st.info("""
        **How to use:**
        - Paste your backlink URLs below (one per line)
        - Click "Analyze Backlinks" to get quality assessment
        - Review the results and export to CSV if needed
        """)
        
        input_urls = st.text_area(
            "Enter Backlink URLs (one per line)",
            height=300,
            placeholder="https://example.com/page1\nhttps://example.com/page2\nhttps://example.com/page3\nhttps://spam-network-example.com/link\nhttps://christmas-blog-spam.com/post"
        )
        
        analyze_button = st.button("Analyze Backlinks", type="primary", use_container_width=True)
        
        if analyze_button:
            if not input_urls.strip():
                st.warning("Please enter at least one URL.")
            else:
                st.session_state.input_urls = input_urls # Save for re-run
                urls = [url.strip() for url in input_urls.split('\n') if url.strip()]
                
                with st.spinner("Analyzing backlinks..."):
                    analyzed_links = [analyze_url(url) for url in urls]
                    st.session_state.backlinks_df = pd.DataFrame(analyzed_links)
                
                # Re-run the script to show the results page
                st.rerun()

# --- Results Screen ---
else:
    df = st.session_state.backlinks_df.copy() # Use a copy to avoid changing session state
    
    # --- Add "No." column ---
    df.insert(0, 'No.', range(1, len(df) + 1))
    
    # --- Summary Metrics ---
    st.subheader("Analysis Summary")
    actions = df['Action'].value_counts()
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Links", len(df))
    col2.metric("Maintain", actions.get('Maintain', 0))
    col3.metric("Disavow", actions.get('Disavow', 0))
    col4.metric("Monitor", actions.get('Monitor', 0))
    col5.metric("Review", actions.get('Review', 0))

    # --- Actions and Filtering ---
    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            search_term = st.text_input("Search backlinks...", placeholder="Search domain, assessment, etc.")
        
        with col2:
            # Prepare CSV data
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Export CSV",
                data=csv_data,
                file_name="backlink-analysis.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col3:
            if st.button("Reset", use_container_width=True):
                st.session_state.backlinks_df = None
                st.session_state.input_urls = ""
                st.rerun()

    # --- Data Table ---
    st.subheader("Analyzed Backlinks")
    
    # Filter dataframe
    if search_term:
        # Simple string search across all columns
        mask = df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)
        filtered_df = df[mask]
    else:
        filtered_df = df

    # Display the dataframe with styling and new column order
    st.dataframe(
        filtered_df.style.applymap(get_color_style, subset=['Quality', 'Domain Authority']),
        # Reorder columns as requested
        column_order=(
            'No.', 
            'URL', 
            'Domain', 
            'Quality', 
            'Domain Authority', 
            'Link Type', 
            'Action', 
            'Assessment', 
            'Recommendation'
        ),
        use_container_width=True,
        hide_index=True
    )
