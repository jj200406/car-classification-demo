import streamlit as st
import requests
st.set_page_config( page_title="Car vs Not Car", page_icon="🚗", layout="centered" )
st.title("🚗 Car vs Not Car") 
st.subheader("AI Image Classification Demo")
st.write( "Upload an image and let the AI model determine " "whether it contains a car." )
uploaded_file = st.file_uploader( "Choose an image", type=["jpg", "jpeg", "png"] )
if uploaded_file is not None:
    st.image(
      uploaded_file,
      caption="Uploaded Image",
      width="stretch"
)

  if st.button("🔍 Classify Image", width="stretch"):

    endpoint = st.secrets["CUSTOM_VISION_URL"]
    prediction_key = st.secrets["CUSTOM_VISION_KEY"]

    image_data = uploaded_file.getvalue()

    headers = {
        "Prediction-Key": prediction_key,
        "Content-Type": "application/octet-stream"
    }

    response = requests.post(
        endpoint,
        headers=headers,
        data=image_data
    )

    if response.status_code == 200:

        result = response.json()
        predictions = result["predictions"]

        best_prediction = max(
            predictions,
            key=lambda x: x["probability"]
        )

        tag = best_prediction["tagName"]
        probability = best_prediction["probability"]

        st.success(
            f"Prediction: {tag}"
        )

        st.metric(
            "Confidence",
            f"{probability:.2%}"
        )

        st.progress(probability)

    else:
        st.error(
            f"Prediction failed: {response.status_code}"
        )
