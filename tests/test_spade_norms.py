#!/usr/bin/env python

"""Tests for `spade_norms` package."""

import pytest


from spade_norms import spade_norms

#Factory_boy
#conftest.py -> te permite definir fixtures (parametros a pasarle alos test si te hace falta) 

@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

# list of things to test:
# file: spade_norms.py
#   __check_exists() -> raise exception when action not found. Nothing otherwise
#   add_action() -> adds action if not there
#   add_action() -> updates action if there
#   
# file: normative_response.py
#   add_allowing_norm() -> if [] responsetype = allowed
#   add_allowing_norm() -> if [ALLOWED] responsetype = allowed
#   add_allowing_norm() -> if [FORBIDDEN] responsetype = forbidden
#   add_allowing_norm() -> if [INVIOLABLE] responsetype = inviolable
#   add_allowing_norm() -> if [] responsetype = allowed
#   
#   add_forbidding_norm() -> if [] responsetype = forbidden
#   add_forbidding_norm() -> if [ALLOWED] responsetype = forbidden
#   add_forbidding_norm() -> if [FORBIDDEN] responsetype = forbidden
#   add_forbidding_norm() -> if [INVIOLABLE] responsetype = inviolable
#
#   add_allowing_norm(inviolable_norm) -> if [] responsetype = allowed
#   add_allowing_norm(inviolable_norm) -> if [ALLOWED] responsetype = allowed
#   add_allowing_norm(inviolable_norm) -> if [FORBIDDEN] responsetype = forbidden
#   add_allowing_norm(inviolable_norm) -> if [INVIOLABLE] responsetype = inviolable
#   add_allowing_norm(inviolable_norm) -> if [] responsetype = allowed
#   
#   add_forbidding_norm(inviolable_norm) -> if [] responsetype = forbidden
#   add_forbidding_norm(inviolable_norm) -> if [ALLOWED] responsetype = forbidden
#   add_forbidding_norm(inviolable_norm) -> if [FORBIDDEN] responsetype = forbidden
#   add_forbidding_norm(inviolable_norm) -> if [INVIOLABLE] responsetype = inviolable
#
# file: norm_engine.py
#   add_norms() -> list of non domained actions - over empt dict
#   add_norms() -> list of domained actions - over empt dict
#   add_norms() -> list of domained and non domained actions - over empt dict
#   add_norms() -> list of non domained actions - over existing dict
#   add_norms() -> list of domained actions - over existing dict
#   add_norms() -> list of domained and non domained actions - over existing dict
#
#   add_norm() -> no domain, no previous norm
#   add_norm() -> no domain, previous norm withoud domain
#   add_norm() -> no domain, previous norm with domain
#   add_norm() -> domain, no previous norm
#   add_norm() -> domain, previous norm withoud domain
#   add_norm() -> domain, previous norm with domain
#
#   filter_norms_by_role() -> role= None
#   filter_norms_by_role() -> norm_list = []
#   filter_norms_by_role() -> role in norm_list
#   filter_norms_by_role() -> role NOT in norm_list
#
#
