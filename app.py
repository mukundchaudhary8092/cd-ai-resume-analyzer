import streamlit as st
import re
from pypdf import PdfReader

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
)

# App title
st.title("📄 AI Resume Analyzer")
st.write("Upload your resume to analyze your skills and resume quality.")

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:
    try:
        # Read PDF
        reader = PdfReader(uploaded_file)
        resume_text = ""

        for page in reader.pages:
            resume_text += page.extract_text() or ""

        # Check extracted text
        if not resume_text.strip():
            st.warning("No text found. This PDF may be scanned.")

        else:
            st.success("Resume uploaded successfully!")

            # Extracted text
            st.subheader("📄 Extracted Resume Text")
            st.text_area(
                "Your resume content",
                resume_text,
                height=250
            )

            # Convert text to lowercase
            text_lower = resume_text.lower()

            # --------------------------------
            # SKILLS ANALYSIS
            # --------------------------------

            st.divider()
            st.subheader("📊 Resume Skills Analysis")

            skills = [
                "python",
                "java",
                "c++",
                "c",
                "html",
                "css",
                "javascript",
                "react",
                "node.js",
                "sql",
                "mysql",
                "mongodb",
                "machine learning",
                "deep learning",
                "data analysis",
                "pandas",
                "numpy",
                "excel",
                "power bi",
                "tableau",
                "git",
                "github",
                "linux",
                "aws",
                "docker",
                "communication",
                "teamwork",
                "problem solving"
            ]

            found_skills = []

            for skill in skills:
                pattern = (
                    r"(?<!\w)"
                    + re.escape(skill)
                    + r"(?!\w)"
                )

                if re.search(pattern, text_lower):
                    found_skills.append(skill)

            st.write("### ✅ Skills Found")

            if found_skills:
                st.success(
                    "Found Skills: " +
                    ", ".join(found_skills)
                )
            else:
                st.info(
                    "No predefined skills found in this resume."
                )

            # --------------------------------
            # RESUME SCORE
            # --------------------------------

            st.divider()
            st.subheader("🎯 Resume Score")

            word_count = len(resume_text.split())

            score = 0

            # Skills score
            if len(found_skills) >= 8:
                score += 30
            elif len(found_skills) >= 5:
                score += 25
            elif len(found_skills) >= 3:
                score += 20
            elif len(found_skills) >= 1:
                score += 10

            # Word count score
            if word_count >= 500:
                score += 25
            elif word_count >= 300:
                score += 20
            elif word_count >= 150:
                score += 15
            else:
                score += 5

            # Section score
            sections = [
                "education",
                "experience",
                "project",
                "skills"
            ]

            sections_found = 0

            for section in sections:
                if section in text_lower:
                    sections_found += 1

            score += sections_found * 10

            # Final score
            score = min(score, 100)

            st.metric(
                "Resume Score",
                f"{score}/100"
            )

            # Progress bar
            st.progress(score / 100)

            # --------------------------------
            # RESUME SUMMARY
            # --------------------------------

            st.divider()
            st.subheader("📄 Resume Summary")

            st.write(
                f"**Total words:** {word_count}"
            )

            st.write(
                f"**Skills detected:** {len(found_skills)}"
            )

            st.write(
                f"**Sections detected:** "
                f"{sections_found}/{len(sections)}"
            )

            # --------------------------------
            # SUGGESTIONS
            # --------------------------------

            st.subheader("💡 Suggestions")

            suggestions = []

            if word_count < 150:
                suggestions.append(
                    "Add more details about projects and experience."
                )

            if "project" not in text_lower:
                suggestions.append(
                    "Add a Projects section."
                )

            if "education" not in text_lower:
                suggestions.append(
                    "Add an Education section."
                )

            if "experience" not in text_lower:
                suggestions.append(
                    "Add an Experience section."
                )

            if "skills" not in text_lower:
                suggestions.append(
                    "Add a dedicated Skills section."
                )

            if len(found_skills) < 5:
                suggestions.append(
                    "Add more relevant technical and soft skills."
                )

            if suggestions:
                for suggestion in suggestions:
                    st.write("• " + suggestion)
            else:
                st.success(
                    "Great! Your resume structure looks good."
                )

            # --------------------------------
            # FINAL MESSAGE
            # --------------------------------

            st.success(
                "🎉 Resume analysis completed successfully!"
            )

    except Exception as e:
        st.error(
            f"Could not read the PDF: {e}"
        )