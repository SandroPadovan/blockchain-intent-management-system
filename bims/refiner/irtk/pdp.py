import logging

import requests
from requests import Response

from .config import PDP_API_ENDPOINT_URI
from .policy import Policy

LOGGER = logging.getLogger(__name__)


def create_policy(policy: Policy) -> Response:
    policy_dict = policy.asdict()
    LOGGER.info("creating new policy: %s", policy_dict)
    response = requests.post(f"{PDP_API_ENDPOINT_URI}/policies", policy_dict)

    try:
        response.raise_for_status()
    except requests.HTTPError:
        # TODO handle creation error
        LOGGER.warning("could not create policy: %s", response.text)

    return response
