import json
from typing import Dict, Optional, Tuple

import streamlit as st

from simpoll.models import Question
from simpoll.frontend.helpers import (
    JsonWebToken,
    sidebar_menu,
    redirect,
)


def question_configs(question_config_form, configs: Dict, jwt_instance: JsonWebToken) -> Tuple[bool, Dict]:
    with question_config_form.form("question-config-form", clear_on_submit=False):
        question_config = st.text_input(label="Question Config")
        submitted = st.form_submit_button("Retrieve")
    if submitted:
        configs["question_configs"] = question_config
        question_config_form.empty()
    return submitted, configs


def view(configs: Dict, jwt_instance: JsonWebToken):
    sidebar_menu(
        configs=configs,
        jwt_instance=jwt_instance,
    )
    question_config_form = st.empty()
    display, configs = question_configs(
        configs=configs,
        jwt_instance=jwt_instance,
        question_config_form=question_config_form,
    )
    if not display:
        return configs
    question_config_form.empty()
    redirect(
        name="question_display",
        configs=configs,
        jwt_instance=jwt_instance,
    )
    st.experimental_rerun()
