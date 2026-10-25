
import re
import streamlit as st

# Configure the application
st.set_page_config(
    page_title="Inkloom AI",
    page_icon="📝",
    layout="wide"
)

# Main heading
st.title("Inkloom AI")
st.subheader("Brand Content Checker")

st.write(
    "Check your content against your brand guidelines "
    "before publishing it."
)

# ---------------------------------
# 1. BRAND GUIDELINES
# ---------------------------------

st.header("1. Brand Guidelines")

brand_name = st.text_input(
    "Brand name",
    placeholder="Example: ABC Company"
)

approved_products = st.text_input(
    "Approved product names (comma-separated)",
    placeholder="Smart Watch, Smart Band"
)

prohibited_words = st.text_input(
    "Prohibited words (comma-separated)",
    placeholder="Cheap, Worst"
)

required_phrase = st.text_input(
    "Required phrase (optional)",
    placeholder="Example: Terms and conditions apply"
)

# ---------------------------------
# 2. CONTENT INPUT
# ---------------------------------

st.header("2. Content Review")

content = st.text_area(
    "Enter the content you want to check",
    height=200,
    placeholder="Paste your advertisement or social media post here."
)

# ---------------------------------
# 3. HELPER FUNCTIONS
# ---------------------------------

def split_items(text):
    """Convert comma-separated input into a clean list."""
    return [
        item.strip()
        for item in text.split(",")
        if item.strip()
    ]


def contains_phrase(text, phrase):
    """Check whether a phrase appears as a separate phrase."""
    pattern = (
        r"(?<!\w)"
        + re.escape(phrase)
        + r"(?!\w)"
    )

    return re.search(
        pattern,
        text,
        flags=re.IGNORECASE
    ) is not None


def check_content(
    text,
    approved_products,
    prohibited_words,
    required_phrase
):
    """Check submitted content against the supplied rules."""

    issues = []

    # Check prohibited words
    for word in prohibited_words:
        if contains_phrase(text, word):
            issues.append({
                "type": "Prohibited word",
                "problem": f'The word or phrase "{word}" is not allowed.',
                "suggestion": (
                    f'Review "{word}" and replace it with '
                    "wording approved by your brand."
                )
            })

    # Check approved product names
    for product in approved_products:
        if contains_phrase(text, product):
            continue

        issues.append({
            "type": "Product name",
            "problem": (
                f'The approved product name "{product}" '
                "was not found in the content."
            ),
            "suggestion": (
                "Check whether this product should be mentioned "
                "and use its exact approved name when needed."
            )
        })

    # Check required phrase
    if required_phrase and not contains_phrase(
        text,
        required_phrase
    ):
        issues.append({
            "type": "Missing required phrase",
            "problem": (
                f'The required phrase "{required_phrase}" '
                "was not found."
            ),
            "suggestion": (
                "Add the required phrase if it applies to this content."
            )
        })

    # Flag claims that may need evidence
    risky_phrases = [
        "100% guaranteed",
        "guaranteed results",
        "cures every disease",
        "no risk at all",
        "best in the world"
    ]

    for phrase in risky_phrases:
        if contains_phrase(text, phrase):
            issues.append({
                "type": "Claim needs review",
                "problem": (
                    f'The claim "{phrase}" may need '
                    "supporting evidence or approval."
                ),
                "suggestion": (
                    "Verify the claim against an approved source "
                    "or rewrite it more carefully."
                )
            })

    return issues


# ---------------------------------
# 4. CHECK CONTENT
# ---------------------------------

if st.button("Check Content"):

    if not brand_name.strip():
        st.warning("Please enter your brand name.")

    elif not content.strip():
        st.warning("Please enter some content to check.")

    else:
        products = split_items(approved_products)
        blocked_words = split_items(prohibited_words)

        results = check_content(
            content,
            products,
            blocked_words,
            required_phrase.strip()
        )

        st.divider()
        st.header("3. Review Results")

        st.write(f"**Brand:** {brand_name}")

        if not products and not blocked_words and not required_phrase.strip():
            st.info(
                "You have not added product-name, prohibited-word "
                "or required-phrase rules. Only promotional claim "
                "checks can run."
            )

        if results:
            st.warning(
                f"{len(results)} issue(s) need your attention."
            )

            for number, issue in enumerate(results, start=1):
                with st.expander(
                    f"{number}. {issue['type']}"
                ):
                    st.write("**Issue:**", issue["problem"])
                    st.write(
                        "**Suggested action:**",
                        issue["suggestion"]
                    )

            st.info(
                "Review the findings before publishing. "
                "Some findings may not apply to every piece of content."
            )

        else:
            st.success(
                "No issues were found by the current rules."
            )

        st.subheader("Submitted Content")
        st.write(content)