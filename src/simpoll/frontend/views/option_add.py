import json
import textwrap
from typing import Dict

import streamlit as st

from simpoll.models import Question, Option
from simpoll.frontend.helpers import (
    JsonWebToken,
    sidebar_menu,
    redirect,
)


def view(configs: Dict, jwt_instance: JsonWebToken):
    sidebar_menu(
        configs=configs,
        jwt_instance=jwt_instance,
    )
    question = Question.from_payload(payload=json.dumps(configs["question"]))
    st.header("Register Option")
    option_num = len(question.options) + 1
    with st.form(f"option-{option_num}", clear_on_submit=False):
        option = st.text_input(f"Register option {option_num}")
        is_correct = st.checkbox("Is Correct")
        submitted = st.form_submit_button("Register")
    if not submitted:
        question_info = jwt_instance.encode(payload={"q": question}, json_encoder=Question.Encoder)
        st.markdown(
            textwrap.dedent(
                f"""
                Question Config:
                
                ```text
                {question_info}
                ```
                """
            )
        )
        st.header(f"Q: {question.question}")
        sep = "\n* "
        options = sep + sep.join(f"{opt.content} {'(correct)' if opt.is_correct else ''}" for opt in question.options)
        st.markdown(options)
        return configs
    # Assign option to question
    question.create_and_assign_option(
        content=option,
        is_correct=is_correct
    )
    # Redirect
    redirect(
        name="add_options",
        configs={
            **configs,
            "question": question,
        },
        jwt_instance=jwt_instance,
        json_encoder=Question.Encoder,
    )
    st.experimental_rerun()
