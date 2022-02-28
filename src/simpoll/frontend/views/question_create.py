from typing import Dict

import streamlit as st

from simpoll.models import Question
from simpoll.frontend.helpers import (
    JsonWebToken,
    sidebar_menu,
    redirect,
)


def create_question():
    with st.form("question", clear_on_submit=False):
        question = st.text_input(label="Question")
        description = st.text_input(label="Description", value="")
        choices = int(st.text_input(label="Number of Correct Options", value="1"))
        submitted = st.form_submit_button("Create")
    if not submitted:
        return
    return Question(
        question=question,
        description=description,
        correct_choices=choices,
    )


def view(configs: Dict, jwt_instance: JsonWebToken):
    sidebar_menu(
        configs=configs,
        jwt_instance=jwt_instance,
    )
    st.header("Create New Question")
    question = create_question()
    if not question:
        return configs
    redirect(
        name="option_add",
        configs={
            "question": question,
            **configs,
        },
        jwt_instance=jwt_instance,
        json_encoder=Question.Encoder,
    )
    st.experimental_rerun()
