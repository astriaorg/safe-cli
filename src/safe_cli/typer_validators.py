import os
from binascii import Error
from typing import List

import click
import typer
from eth_account import Account
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3


def validate_eth_address(address: str) -> ChecksumAddress:
    """Validate Ethereum address checksum."""
    if not Web3.is_checksum_address(address):
        raise typer.BadParameter("Invalid Ethereum address")
    return address


class ChecksumAddressParser(click.ParamType):
    name = "ChecksumAddress"

    def convert(self, value, param, ctx):
        """
        ChecksumAddress parser from str
        """
        return ChecksumAddress(value)


def validate_private_keys(private_keys: List[str]) -> List[str]:
    """Validate list of private keys."""
    if not private_keys:
        raise typer.BadParameter("At least one private key is required")
    
    for key in private_keys:
        try:
            Account.from_key(key)
        except (ValueError, TypeError):
            raise typer.BadParameter(f"Invalid private key: {key}")
    return private_keys


def validate_hex(hex_str: str) -> HexBytes:
    """Validate hexadecimal string."""
    try:
        return HexBytes(hex_str)
    except ValueError:
        raise typer.BadParameter(f"Invalid hexadecimal string: {hex_str}")


class HexBytesParser(click.ParamType):
    name = "HexBytes"

    def convert(self, value, param, ctx):
        """
        HexBytes string parser from str
        """
        return HexBytes(value)
