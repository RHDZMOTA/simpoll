
import streamlit as st

from .helpers import (
    JsonWebToken,
    next_page,
)


@st.cache
def get_jwt_instance() -> JsonWebToken:
    return JsonWebToken.auto_configure()


def main():
    jwt_instance = get_jwt_instance()
    query_params = st.experimental_get_query_params()
    # Retrieve view name & configs from query params
    view, *_ = query_params.get("view", ["question_configs"])
    configs_encoded, *_ = query_params.get("configs", [None])
    # Decode config object or default to empty configuration
    configs = jwt_instance.decode(string=configs_encoded) if configs_encoded else {}
    # Load view & content
    next_page(name=view, configs=configs, jwt_instance=jwt_instance)

