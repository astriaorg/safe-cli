import os
from binascii import Error
from typing import List

import click
import typer
from eth_account import Account
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3


def check_ethereum_address(addr: str) -> ChecksumAddress:
    if not Web3.is_checksum_address(addr):
        raise typer.BadParameter("Invalid ethereum address")
    return ChecksumAddress(addr)


class ChecksumAddressParser(click.ParamType):
    def convert(self, value, *_):
        return ChecksumAddress(value)


def check_private_keys(keys: List[str]) -> List[str]:
    if keys is None:
        raise typer.BadParameter("At least one private key is required")
    for key in keys:
        try:
            Account.from_key(os.environ.get(key, default=key))
        except (ValueError, Error):
            raise typer.BadParameter(f"{key} is not a valid private key")
    return keys


def check_hex_str(hex_str: str) -> HexBytes:
    try:
        return HexBytes(hex_str)
    except ValueError:
        raise typer.BadParameter(f"{hex_str} is not a valid hexadecimal string")


class HexBytesParser(click.ParamType):
    def convert(self, value, *_):
        return HexBytes(value)
