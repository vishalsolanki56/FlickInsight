import streamlit as st
from moviewApp import scrape_movie_reviews, textrank_summarize, text_preprocess, generate_summary, get_sentiment_score

# Set page config to wide layout
st.set_page_config(layout="wide")

def analyze_movie(movie_name):
    # Scrape movie reviews
    print("Analyse Movie Method Started");
    scrape_movie_reviews(movie_name)

    # Load and preprocess scraped reviews
    file_path = 'movie_review.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    textrank_summary = textrank_summarize(text, 0.7)
    preprocessed_text = text_preprocess(textrank_summary)

    # Generate summary and calculate sentiment score
    summary = generate_summary(preprocessed_text)
    sentiment_score = get_sentiment_score(summary)
    print("Analyse Movie Method Ended");
    return summary, sentiment_score

# Custom CSS to style the FlickInsight title
st.markdown(
    """
    <style>
    .title-wrapper .typography .stMarkdown {
        color: purple !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns(2)
with left:
    # Streamlit UI
    st.title(':violet[FlickInsight]: _AI Movie Review App_')

    movie_name = st.text_input("Enter the name of the movie here:", "")

    if st.button("Analyze"):
        with st.spinner('Analyzing...'):
            summary, sentiment_score = analyze_movie(movie_name)

            # Display summary with italic font
            st.write("Review:")
            st.markdown(f"*{summary}*", unsafe_allow_html=True)

            # Display sentiment score with 2 decimal points and in bold font
            st.write(f"Sentiment score out of 10: **{sentiment_score:.2f}**")

            # Display sentiment meter (gauge)
            st.write("Sentiment Meter:")
            st.progress(sentiment_score / 10)
with right:
    st.image("movieTiles.jpg", use_column_width=True)