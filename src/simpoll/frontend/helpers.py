import os
import json
import importlib
from typing import Callable, Dict, List, Optional, Type

import jwt
import streamlit as st

from simpoll.settings import (
    SIMPOLL_JWT_ENCRYPTION_ALGORITHM,
    get_jwt_secret_key,
    get_logger,
)


logger = get_logger(name=__name__)


def get_view_callable(name: str) -> Callable:
    module = importlib.import_module(f"simpoll.frontend.views.{name}")
    return getattr(module, "view")


class JsonWebToken:

    def __init__(
            self,
            secret_key: str,
            algorithm: Optional[str] = None,
            verify_exp: bool = False,
    ):
        self._secret_key = secret_key
        self.verify_exp = verify_exp
        self.algorithm = algorithm or SIMPOLL_JWT_ENCRYPTION_ALGORITHM

    @staticmethod
    def auto_configure() -> 'JsonWebToken':
        return JsonWebToken(secret_key=get_jwt_secret_key(), algorithm=SIMPOLL_JWT_ENCRYPTION_ALGORITHM)

    def encode(self, payload: Dict, json_encoder: Optional[Type[json.JSONEncoder]] = None) -> str:
        # Read more here: https://pyjwt.readthedocs.io/en/latest/usage.html
        return jwt.encode(payload, key=self._secret_key, algorithm=self.algorithm, json_encoder=json_encoder)

    def decode(self, string: str) -> Dict:
        return jwt.decode(
            jwt=string,
            key=self._secret_key,
            algorithms=[self.algorithm],
            options={
                "verify_exp": self.verify_exp
            }
        )



def redirect(
        name: str,
        configs: Dict,
        jwt_instance: JsonWebToken,
        json_encoder: Optional[Type[json.JSONEncoder]] = None,
):
    st.experimental_set_query_params(
        view=name,
        configs=jwt_instance.encode(
            payload=configs,
            json_encoder=json_encoder,
        )
    )


def next_page(
        name: str,
        configs: Dict,
        jwt_instance: JsonWebToken,
        json_encoder: Optional[Type[json.JSONEncoder]] = None,
):
    view_callable = get_view_callable(name=name)
    # Redirect updates the query params values
    redirect(
        name=name,
        # Executing the view-callable before redirect loads the new content
        configs=view_callable(configs=configs, jwt_instance=jwt_instance),
        jwt_instance=jwt_instance,
        json_encoder=json_encoder,
    )


def validate_param(
        name: str,
        configs: Dict,
        next_view: Callable,
        label: Optional[str] = None
) -> Dict:
    label = label or name
    if name not in configs.keys():
        param_form = st.empty()
        with param_form.form(key="parameter-validation-from"):
            code = st.text_input(label=label)
            if code:
                configs[name] = code
            submitted = st.form_submit_button('Submit')
        if submitted:
            param_form.empty()
            return next_view(configs)
        return configs
    else:
        return next_view(configs=configs)


def validate_param_metadecorator(name: str, label: Optional[str] = None):
    def decorator(func: Callable):
        def wrapper(configs: Dict) -> Dict:
            return validate_param(
                name=name,
                configs=configs,
                next_view=func,
                label=label,
            )
        return wrapper
    return decorator


def sidebar_menu(
        configs: Dict,
        jwt_instance: JsonWebToken,
        json_encoder: Optional[Type[json.JSONEncoder]] = None,
):
    query_params = st.experimental_get_query_params()
    current_view, *_ = query_params.get("view", ["current"])
    menu_options = {
        "Create Question": "question_create",
        "Retrieve Question": "question_configs",
    }
    selection = st.sidebar.radio(
        label="Menu",
        key=current_view,
        options=[
            "Current",
            *list(menu_options.keys())
        ],
    )
    current_view_label = f"{current_view} (query params)"
    selection_page = menu_options.get(selection, current_view_label)
    if current_view_label == selection_page or current_view == selection_page:
        logger.debug("Sidebar selection '%s' not redirected.", current_view)
        return
    logger.info("Sidebar redirect from '%s' to '%s'.", current_view, selection_page)
    redirect(
        name=selection_page,
        configs=configs,
        jwt_instance=jwt_instance,
        json_encoder=json_encoder,
    )
    st.experimental_rerun()
