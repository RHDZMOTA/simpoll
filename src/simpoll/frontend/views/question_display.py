import json
import textwrap
from typing import Dict, Optional, Tuple

import streamlit as st

from simpoll.models import Question, Answer
from simpoll.frontend.helpers import (
    JsonWebToken,
    sidebar_menu,
    redirect,
)


def display_question(
        encoded_question_config: str,
        jwt_instance: JsonWebToken
) -> Tuple[bool, Question, Optional[Answer]]:
    question_dict = jwt_instance.decode(string=encoded_question_config)
    question = Question.from_payload(json.dumps(question_dict["q"]))
    st.header(question.question)
    num = question.correct_choices
    options = {opt.uuid: opt for opt in question.options}
    with st.form("display-question-form", clear_on_submit=False):
        selection = st.multiselect(
            f"Select {num} option{'s' if num > 1 else ''}:",
            format_func=lambda opt_uuid: question.option_hashtable.get(opt_uuid).content,
            options=question.option_hashtable,
        )
        show_answers = st.checkbox("Show Answers")
        submitted = st.form_submit_button("Submit")
    if not submitted:
        return show_answers, question, None
    if num > 0 and len(selection) > num:
        st.warning(f"Please select at most {num} option{'s' if num > 1 else ''}")
        return show_answers, question, None
    return show_answers, question, Answer(
        question=question,
        options=[options[opt_uuid] for opt_uuid in selection],
    )


def view(configs: Dict, jwt_instance: JsonWebToken):
    sidebar_menu(
        configs=configs,
        jwt_instance=jwt_instance,
    )
    show_answers, question, answer = display_question(
        encoded_question_config=configs["question_configs"],
        jwt_instance=jwt_instance
    )
    if not answer:
        return configs
    # TODO: Send to the backend
    st.warning("Backend is not implemented; Answer could not be registered.")
    # Display answer
    if not question.correct_choices:
        return configs
    if show_answers:
        answers = {opt.uuid for opt in answer.options}
        correct_options = {opt.uuid for opt in question.options}
        correct_answers = len(answers - correct_options)
        st.write(f"Score: {round(100 * correct_answers / len(correct_options), 2)}")
        st.markdown(
            "\n".join(
                f"- [{'X' if opt.uuid in answers else ' '}] {'✔' if opt.is_correct else '❌'} {opt.content}"
                for opt in question.options
            )
        )
        st.json(answer.payload)
    return configs
