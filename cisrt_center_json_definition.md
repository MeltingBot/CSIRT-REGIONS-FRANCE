# Documentation Technique - Schéma JSON des CSIRT France

## Table des matières

1. [Introduction](#introduction)
2. [Structure générale](#structure-générale)
3. [Schéma détaillé](#schéma-détaillé)
4. [Types de données](#types-de-données)
5. [Exemples d'utilisation](#exemples-dutilisation)
6. [Validation des données](#validation-des-données)
7. [Bonnes pratiques](#bonnes-pratiques)
8. [Annexes](#annexes)

## Introduction

Cette documentation décrit le format de données standardisé pour représenter les informations des Centres de réponse aux incidents de sécurité informatique (CSIRT). Ce format est conçu pour faciliter l'interopérabilité et l'exploitation des données des CSIRT.

### Objectifs

- Standardiser la représentation des CSIRT
- Faciliter l'échange de données entre systèmes
- Permettre une interrogation programmatique des informations
- Assurer la cohérence des données

### Version du schéma

- Version : 1.0.0
- Date de dernière mise à jour : 2024-08-15

## Structure générale

```json
{
  "csirt_centers": [
    {
      // Objet CSIRT
    }
  ]
}
```

## Schéma détaillé

### Informations de base

| Champ | Type | Obligatoire | Description | Exemple |
|-------|------|-------------|-------------|---------|
| `name` | string | Oui | Nom officiel du CSIRT | `"CISRT ATLANTIC"` |
| `country` | string | Oui | Code pays ISO 3166-1 alpha-2 | `"FR"` |
| `region` | string | Oui | Région administrative | `"Antilles, Guyane"` |
| `zone` | string\|null | Non | Zone géographique spécifique | `"Guadeloupe, Guyane, Martinique, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"` |

### Contacts

| Champ | Type | Obligatoire | Description | Exemple |
|-------|------|-------------|-------------|---------|
| `phone` | string | Oui | Numéro de téléphone | `"0 805 036 083"` |
| `call_type` | string\|null | Non | Type d'appel | `"toll_free"` |
| `email` | string | Oui | Email de contact | `"contact@csirt.fr"` |
| `website` | string | Oui | Site web | `"https://www.csirt.fr"` |

## Type d'appel (`call_type`)

| Valeur | Description |
|--------|-------------|
| `toll_free` | Numéro vert, gratuit |
| `local_rate` | Prix d'un appel local |
| `shared_cost` | Numéro à coûts partagés |
| `premium` | Numéro surtaxé |
| `fixed_rate` | Tarif fixe |
| `mobile_rate` | Tarif mobile |

### Périmètre d'intervention (`scope`)

```json
{
  "type": "string",
  "audience": "string",
  "sector": "string|null",
  "eligibility": {
    "geographic": "string",
    "organization_types": ["string"],
    "restrictions": "string|null"
  }
}
```

#### Types de périmètre (`scope.type`)

| Valeur | Description |
|--------|-------------|
| `regional` | CSIRT régional |
| `national` | CSIRT national |
| `overseas` | CSIRT outre-mer |
| `sectoral` | CSIRT sectoriel |

#### Public cible (`scope.audience`)

| Valeur | Description |
|--------|-------------|
| `public` | Service public |
| `private` | Service privé |
| `mixed` | Service mixte |

### Disponibilité (`availability`)

```json
{
  "type": "string",
  "timezone": "string",
  "work_days": ["string"],
  "hours": [
    {
      "start": "string",
      "end": "string"
    }
  ],
  "exceptions": ["string"],
  "raw": "string"
}
```

#### Types de disponibilité

| Type | Description |
|------|-------------|
| `business-hours` | Horaires de bureau |
| `24-7` | Service continu |
| `varying-hours` | Horaires variables |
| `business-hours-with-oncall` | Horaires avec astreinte |



### RFC 2350 (`rfc_2350`)

L'objet `rfc_2350` contient les informations définies par la norme RFC 2350 qui décrit les informations que chaque CSIRT doit publier.

```json
{
  "document_url": "string",
  "version": "string",
  "last_updated": "string",
  "tlp_level": "string",
  "team_information": {
    "name": "string",
    "status": "string",
    "address": "string",
    "timezone": "string",
    "operating_hours": "string"
  },
  "services": {
    "reactive": ["string"],
    "proactive": ["string"]
  },
  "incident_reporting": {
    "points_of_contact": {
      "phone": "string",
      "email": "string",
      "web_form": "string"
    },
    "encryption": {
      "pgp_key_available": "boolean",
      "key_id": "string"
    }
  },
  "policies": {
    "types_of_incidents": ["string"],
    "cooperation": ["string"],
    "disclosure": "string"
  }
}
```

#### Informations générales du document

| Champ | Type | Obligatoire | Description | Exemple |
|-------|------|-------------|-------------|---------|
| `document_url` | string | Oui | URL du document RFC 2350 | `"https://example.com/rfc2350.pdf"` |
| `version` | string | Oui | Version du document | `"1.2"` |
| `last_updated` | string | Oui | Date de dernière mise à jour (ISO 8601) | `"2024-03-15"` |
| `tlp_level` | string | Oui | Niveau de classification TLP | `"WHITE"` |

#### Informations sur l'équipe (`team_information`)

| Champ | Type | Description |
|-------|------|-------------|
| `name` | string | Nom officiel de l'équipe |
| `status` | string | Statut TLP du document |
| `address` | string | Adresse postale |
| `timezone` | string | Fuseau horaire (format IANA) |
| `operating_hours` | string | Horaires d'opération |

#### Services (`services`)

Services réactifs (`reactive`) - Exemples de valeurs :
- `"incident_resolution"`
- `"vulnerability_handling"`
- `"artifact_handling"`
- `"incident_analysis"`
- `"incident_coordination"`

Services proactifs (`proactive`) - Exemples de valeurs :
- `"security_monitoring"`
- `"threat_intelligence"`
- `"security_audits"`
- `"tool_development"`
- `"training_awareness"`

#### Signalement d'incidents (`incident_reporting`)

Points de contact :
```json
{
  "points_of_contact": {
    "phone": "string",
    "email": "string",
    "web_form": "string"
  }
}
```

Chiffrement :
```json
{
  "encryption": {
    "pgp_key_available": boolean,
    "key_id": "string"
  }
}
```

#### Politiques (`policies`)

| Champ | Type | Description |
|-------|------|-------------|
| `types_of_incidents` | array | Types d'incidents traités |
| `cooperation` | array | Partenaires de coopération |
| `disclosure` | string | Politique de divulgation |


### Validation du RFC 2350

Ajout au schéma JSON de validation :

```json
{
  "properties": {
    "rfc_2350": {
      "type": "object",
      "required": ["document_url", "version", "last_updated", "tlp_level"],
      "properties": {
        "document_url": {
          "type": "string",
          "format": "uri"
        },
        "version": {
          "type": "string",
          "pattern": "^\\d+\\.\\d+(\\.\\d+)?$"
        },
        "last_updated": {
          "type": "string",
          "format": "date"
        },
        "tlp_level": {
          "type": "string",
          "enum": ["WHITE", "GREEN", "AMBER", "RED"]
        }
      }
    }
  }
}
```

## Types de données

### Formats standards

- **Dates** : ISO 8601 (`YYYY-MM-DD`)
- **Heures** : Format 24h (`HH:mm`)
- **Fuseaux horaires** : Format IANA (`Europe/Paris`)
- **Codes pays** : ISO 3166-1 alpha-2
- **Email** : Format RFC 5322
- **URL** : Format RFC 3986

### Énumérations

#### Jours de la semaine
```javascript
const weekDays = [
  "monday", "tuesday", "wednesday", "thursday",
  "friday", "saturday", "sunday"
];
```


#### Types d'organisations
```javascript
const organizationTypes = [
  "companies",
  "public_institutions",
  "associations",
  "telecom_operators",
  "healthcare_providers",
  "educational_institutions",
  "local_authorities"
];
```


## Changements de version

### v1.0.0 (2024-08-15)
- Version initiale
- Structure de base
- Support des horaires

Cette documentation est un document vivant destiné à évoluer avec les besoins des utilisateurs et les modifications du schéma.