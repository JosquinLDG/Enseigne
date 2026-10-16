"""
Classe : VendeurResponsable
Module : enseigne.vendeur_responsable
Description : Représente un vendeur responsable d'un secteur au sein d'une enseigne de sport.
"""

from datetime import datetime, timezone

from enseigne.rayon import Rayon
from enseigne.vendeur import Vendeur


class VendeurResponsable(Vendeur):
    def __init__(
        self,
        nom: str,
        prenom: str,
        tel: str,
        email: str,
        prise_fonction: datetime,
        indice_salaire: int,
        rayon: Rayon,
        secteur: str,
        cumul_ventes: float = 0.0,
    ) -> None:
        """Constructeur de la classe VendeurResponsable.

        Args:
            nom: Nom du vendeur responsable.
            prenom: Prénom du vendeur responsable.
            tel: Numéro de téléphone du vendeur responsable.
            email: Email du vendeur responsable dans l'enseigne.
            prise_fonction: Moment où le vendeur responsable commence officiellement à exercer son poste.
            indice_salaire: Indice de la grille de salaire.
            rayon: Rayon auquel est assigné le vendeur responsable.
            secteur: Secteur dont le vendeur responsable a la charge.
            cumul_ventes: Montant cumulé de ses ventes.
        """
        super().__init__(
            nom=nom,
            prenom=prenom,
            tel=tel,
            email=email,
            prise_fonction=prise_fonction,
            indice_salaire=indice_salaire,
            rayon=rayon,
            cumul_ventes=cumul_ventes,
        )
        self.secteur = secteur

    def __str__(self) -> str:
        return f"{self.nom} {self.prenom}, secteur : {self.secteur}"


if __name__ == "__main__":
    r1 = Rayon("VTT")
    vr1 = VendeurResponsable(
        prenom="Jean",
        nom="Benguigui",
        tel="0624567267",
        email="Benguigui@gmail.com",
        prise_fonction=datetime.now(tz=timezone.utc),
        rayon=r1,
        indice_salaire=1,
        secteur="Cyclisme",
    )
    print(vr1)