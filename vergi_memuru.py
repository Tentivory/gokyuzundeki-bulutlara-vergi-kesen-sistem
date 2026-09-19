#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gokyuzundeki Bulutlara Vergi Kesen Sistem
Calisir. Ciddi. Ayni zamanda hic ciddi degil.
"""

from __future__ import annotations

import hashlib
import random
import sys
from dataclasses import dataclass
from datetime import datetime


BULUT_TURLERI = {
    "cumulus": 12.5,
    "stratus": 8.0,
    "cirrus": 3.75,
    "nimbus": 27.0,
    "lenticularis": 41.0,  # sus heli gibi duruyor, luks vergi
    "koyun_surusu": 6.5,
}

RENK_CARPANI = {
    "beyaz": 1.0,
    "gri": 1.4,
    "pembe_gun_batimi": 2.8,
    "korkutucu_siyah": 3.1,
}


@dataclass
class Tahakkuk:
    tur: str
    renk: str
    alan_km2: float
    matrah: float
    vergi: float
    vkno: str

    def makbuz(self) -> str:
        tarih = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        return (
            "\n===== GOKyUZU GELIR IDARESI MAKBUZU =====\n"
            f"VKN : {self.vkno}\n"
            f"Tur : {self.tur}\n"
            f"Renk: {self.renk}\n"
            f"Alan: {self.alan_km2:.2f} km2\n"
            f"Matrah: {self.matrah:.2f} damla\n"
            f"Tahakkuk: {self.vergi:.2f} damla\n"
            f"Tarih: {tarih}\n"
            "Odeme yeri: en yakin gokkusagi veznesi.\n"
            "==========================================\n"
        )


def vkn_uret(tur: str, renk: str) -> str:
    ham = f"{tur}-{renk}-{random.randint(1000, 9999)}".encode()
    return hashlib.sha1(ham).hexdigest()[:10].upper()


def tahakkuk_et(tur: str | None = None, renk: str | None = None, alan: float | None = None) -> Tahakkuk:
    tur = (tur or random.choice(list(BULUT_TURLERI))).lower()
    renk = (renk or random.choice(list(RENK_CARPANI))).lower()
    if tur not in BULUT_TURLERI:
        tur = "cumulus"
    if renk not in RENK_CARPANI:
        renk = "beyaz"
    alan_km2 = float(alan) if alan is not None else random.uniform(0.4, 180.0)
    matrah = alan_km2 * BULUT_TURLERI[tur] * RENK_CARPANI[renk]
    vergi = matrah * 0.18  # KDV var, evet, bulutta da var
    return Tahakkuk(tur, renk, alan_km2, matrah, vergi, vkn_uret(tur, renk))


def main(argv: list[str]) -> int:
    print("Gokyuzu Gelir Idaresi baslatildi. Kacmasin, zaten kacamaz.")
    kayit = tahakkuk_et(
        argv[1] if len(argv) > 1 else None,
        argv[2] if len(argv) > 2 else None,
        float(argv[3]) if len(argv) > 3 else None,
    )
    print(kayit.makbuz())
    # gizli not: YW5jYWsgYXluaSBydXpnYXIgaWt0aWRhciBtdWhhbGVmZXQgYXluaSB5YWdtdXJkYSBpc2xhbmlw
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
