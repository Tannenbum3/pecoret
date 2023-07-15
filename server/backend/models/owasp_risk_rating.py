from django.db import models

RISK_INFORMATIONAL = "Informational"
RISK_LOW = "Low"
RISK_MEDIUM = "Medium"
RISK_HIGH = "High"
RISK_CRITICAL = "Critical"


class SkillLevel(models.IntegerChoices):
    """it should be noted, that according to the
    OWASP documentation (https://owasp.org/www-community/OWASP_Risk_Rating_Methodology)
    the order is reversed. This did not make sense to me, since the non-technical skill
    would have the lowest integer assigned.
    """

    NOT_APPLICABLE = 0, "N/A"
    SECURITY_PENETRATION_SKILL = 1, "Security penetration skills"
    NETWORKING_SKILL = 3, "Networking and programming skills"
    ADVANCED_COMPUTER_SKILL = 5, "Advanced computer skills"
    SOME_TECHNICAL_SKILL = 6, "Some technical skills"
    NO_TECHNICAL_SKILL = 9, "No technical skills"


class Motive(models.IntegerChoices):
    NOT_APPLICABLE = 0, "N/A"
    LOW_OR_NO_REWARD = 1, "Low or no reward"
    POSSIBLE_REWARD = 4, "Possible reward"
    HIGH_RWARD = 9, "High reward"


class Opportunity(models.IntegerChoices):
    FULL_ACCESS_OR_EXPENSIVE = 0, "FUll access or expensive resources required"
    SPECIAL_ACCESS = 4, "Special access or resources required"
    SOME_ACCESS = 7, "Some access or resources required"
    NO_ACCESS = 9, "No access or resources required"


class Size(models.IntegerChoices):
    NOT_APPLICABLE = 0, "N/A"
    DEVELOPERS_OR_SYSADMINS = 2, "Developers or system administrators"
    INTRANET_USERS = 4, "Intranet users"
    PARTNERS = 5, "Partners"
    AUTHENTICATED_USERS = 6, "Authenticated users"
    ANONYMOUS_INTERNET_USERS = 9, "Anonymous internet users"


class EaseOfDiscovery(models.IntegerChoices):
    NOT_APPLICABLE = 0, "N/A"
    PRACTICALLY_IMPOSSIBLE = 1, "Practically impossible"
    DIFFICULT = 3, "Difficult"
    EASY = 7, "Easy"
    AUTOMATED = 9, "Automated tools available"


class EaseOfExploit(models.IntegerChoices):
    NOT_APPLICABLE = 0, "N/A"
    THEORETICAL = 1, "Theoretical"
    DIFFICULT = 3, "Difficult"
    EASY = 7, "Easy"
    AUTOMATED = 9, "Automated tools available"


class Awareness(models.IntegerChoices):
    NOT_APPLICABLE = 0, "N/A"
    UNKNOWN = 1, "Unknown"
    HIDDEN = 4, "Hidden"
    OBVIOUS = 6, "Obvious"
    PUBLIC_KNOWLEDGE = 9, "Public Knowledge"


class IntrusionDetection(models.IntegerChoices):
    NOT_APPLICABLE = 0, "N/A"
    ACTIVE_DETECTION = 1, "Active detection in application"
    LOGGED_AND_REVIEWED = 3, "Logged and reviewed"
    LOGGED_NO_REVIEW = 8, "Logged without review"
    NOT_LOGGED = 9, "Not logged"


class LossOfConfidentiality(models.IntegerChoices):
    NOT_APPLICABLE = 0, "N/A"
    MINIMAL_NON_SENSITIVE = 2, "Minimal non-sensitive data disclosed"
    MINIMAL_CRITICAL = (
        6,
        "Minimal critical data or extensive non-sensitive data disclosed",
    )
    EXTENSIVE = 7, "Extensive critical data disclosed"
    ALL = 9, "All data disclosed"


class LossOfIntegrity(models.IntegerChoices):
    NOT_APPLICABLE = 0, "N/A"
    MINIMAL_SLIGHTLY = 1, "Minimal slightly corrupted data"
    MINIMAL_SERIOUSLY = 3, "Minimal seriously corrupted data"
    EXTENSIVE_SLIGHTLY = 5, "Extensive slightly corrupted data"
    EXTENSIVE_SERIOUSLY = 7, "Extensive seriously corrupted data"
    ALL = 9, "All data totally corrupted"


class LossOfAvailability(models.IntegerChoices):
    NOT_APPLICABLE = 0, "N/A"
    MINIMAL_SECONDARY = 1, "Minimal secondary services interrupted"
    MINIMAL_PRIMARY = 5, "Minimal primary or extensive secondary services interrupted"
    EXTENSIVE_PRIMARY = 7, "Extensive primary services interrupted"
    ALL = 9, "All services completely lost"


class LossOfAccountability(models.IntegerChoices):
    NOT_APPLICABLE = 0, "N/A"
    FULLY_TRACEABLE = 1, "Fully traceable"
    POSSIBLY_TRACEABLE = 7, "Possibly traceable"
    ANONYMOUS = 9, "Completely anonymous"


class FinancialDamage(models.IntegerChoices):
    NOT_APPLICABLE = 0, "N/A"
    LESS_THAN_COST = 1, "Less than the cost to fix the vulnerability"
    MINOR = 3, "Minor effect on annual profit"
    SIGNIFICANT = 7, "Significant effect on annual profit"
    BANKRUPTCY = 9, "Bankruptcy"


class ReputationDamage(models.IntegerChoices):
    NOT_APPLICABLE = 0, "N/A"
    MINIMAL = 1, "Minimal damage"
    MAJOR = 4, "Loss of major accounts"
    GOODWILL = 5, "Loss of goodwill"
    BRAND = 9, "Brand damage"


class NonCompliance(models.IntegerChoices):
    NOT_APPLICABLE = 0, "N/A"
    MINOR = 2, "Minor violation"
    CLEAR = 5, "Clear violation"
    HIGH = 7, "High profile violation"


class PrivacyViolation(models.IntegerChoices):
    NOT_APPLICABLE = 0, "N/A"
    ONE = 3, "One individual"
    HUNDREDS = 5, "Hundreds of people"
    THOUSANDS = 7, "Thousands of people"
    MILLIONS = 9, "Millions of people"


class OWASPRiskRatingQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(finding__project=project)


class OWASPRiskRating(models.Model):
    objects = OWASPRiskRatingQuerySet.as_manager()
    finding = models.OneToOneField("backend.Finding", on_delete=models.CASCADE)
    skill_level = models.PositiveSmallIntegerField(
        choices=SkillLevel.choices, default=SkillLevel.NOT_APPLICABLE
    )
    motive = models.PositiveSmallIntegerField(
        choices=Motive.choices, default=Motive.NOT_APPLICABLE
    )
    opportunity = models.PositiveSmallIntegerField(
        choices=Opportunity.choices,
        default=Opportunity.FULL_ACCESS_OR_EXPENSIVE,
    )
    size = models.PositiveSmallIntegerField(
        choices=Size.choices, default=Size.NOT_APPLICABLE
    )
    ease_of_discovery = models.PositiveSmallIntegerField(
        choices=EaseOfDiscovery.choices,
        default=EaseOfDiscovery.NOT_APPLICABLE,
    )
    ease_of_exploit = models.PositiveSmallIntegerField(
        choices=EaseOfExploit.choices, default=EaseOfExploit.NOT_APPLICABLE
    )
    awareness = models.PositiveSmallIntegerField(
        choices=Awareness.choices, default=Awareness.NOT_APPLICABLE
    )
    intrusion_detection = models.PositiveSmallIntegerField(
        choices=IntrusionDetection.choices,
        default=IntrusionDetection.NOT_APPLICABLE,
    )
    loss_of_confidentiality = models.PositiveSmallIntegerField(
        choices=LossOfConfidentiality.choices,
        default=LossOfConfidentiality.NOT_APPLICABLE,
    )
    loss_of_availability = models.PositiveSmallIntegerField(
        choices=LossOfAvailability.choices,
        default=LossOfAvailability.NOT_APPLICABLE,
    )
    loss_of_integrity = models.PositiveSmallIntegerField(
        choices=LossOfIntegrity.choices,
        default=LossOfIntegrity.NOT_APPLICABLE,
    )
    loss_of_accountability = models.PositiveSmallIntegerField(
        choices=LossOfAccountability.choices,
        default=LossOfAccountability.NOT_APPLICABLE,
    )
    financial_damage = models.PositiveSmallIntegerField(
        choices=FinancialDamage.choices,
        default=FinancialDamage.NOT_APPLICABLE,
    )
    reputation_damage = models.PositiveSmallIntegerField(
        choices=ReputationDamage.choices,
        default=ReputationDamage.NOT_APPLICABLE,
    )
    non_compliance = models.PositiveSmallIntegerField(
        choices=NonCompliance.choices, default=NonCompliance.NOT_APPLICABLE
    )
    privacy_violation = models.PositiveSmallIntegerField(
        choices=PrivacyViolation.choices,
        default=PrivacyViolation.NOT_APPLICABLE,
    )

    class Meta:
        ordering = ["finding"]

    @property
    def is_incomplete(self):
        if self.technical_impact_factor and self.impact_factors and self.business_impact_factor and self.likelihood_factors:
            return False
        return True

    @property
    def vector(self):
        threat_agent = (
            f"SL:{self.skill_level}/M:{self.motive}/O:{self.opportunity}/S:{self.size}"
        )
        vulnerability = f"ED:{self.ease_of_discovery}/EE:{self.ease_of_exploit}/A:{self.awareness}/ID:{self.intrusion_detection}"
        likelihood = f"{threat_agent}/{vulnerability}"
        technial = f"LC:{self.loss_of_confidentiality}/LI:{self.loss_of_integrity}/LAV:{self.loss_of_availability}/LAC:{self.loss_of_availability}"
        business = f"FD:{self.financial_damage}/RD:{self.reputation_damage}/NC:{self.non_compliance}/PV:{self.privacy_violation}"
        impact = f"{technial}/{business}"
        return f"{likelihood}/{impact}"

    @property
    def technical_impact_factor(self):
        factors = (
                self.loss_of_confidentiality
                + self.loss_of_integrity
                + self.loss_of_availability
                + self.loss_of_accountability
        )
        return factors / 4.0

    @property
    def business_impact_factor(self):
        factors = (
                self.financial_damage
                + self.reputation_damage
                + self.non_compliance
                + self.privacy_violation
        )
        return factors / 4.0

    @property
    def thread_agent_factor(self):
        factors = self.skill_level + self.motive + self.opportunity + self.size
        return factors / 4.0

    @property
    def vulnerability_factor(self):
        factors = (
                self.ease_of_discovery
                + self.ease_of_exploit
                + self.awareness
                + self.intrusion_detection
        )
        return factors / 4.0

    @property
    def likelihood_factors(self):
        factors = (self.thread_agent_factor + self.vulnerability_factor) / 2.0
        if factors < 0.1:
            risk = RISK_INFORMATIONAL
        if factors < 3:
            risk = RISK_LOW
        elif factors < 6:
            risk = RISK_MEDIUM
        elif factors < 9:
            risk = RISK_HIGH
        return factors, risk

    @property
    def impact_factors(self):
        factors = (self.technical_impact_factor + self.business_impact_factor) / 2.0
        if factors < 0.1:
            return factors, RISK_INFORMATIONAL
        if factors < 3:
            return factors, RISK_LOW
        elif factors < 6:
            return factors, RISK_MEDIUM
        return factors, RISK_HIGH

    @property
    def overall_risk_severity(self):
        # FIXME: ugly and needs improvement.
        impact = self.impact_factors
        likelihood = self.likelihood_factors
        if impact[0] < 3:
            if likelihood[1] == RISK_LOW:
                return RISK_INFORMATIONAL
            elif likelihood[1] == RISK_MEDIUM:
                return RISK_LOW
            elif likelihood[1] == RISK_HIGH:
                return RISK_MEDIUM
        elif impact[0] < 6:
            if likelihood[1] == RISK_LOW:
                return RISK_LOW
            elif likelihood[1] == RISK_MEDIUM:
                return RISK_MEDIUM
            elif likelihood[1] == RISK_HIGH:
                return RISK_HIGH
        if likelihood[1] == RISK_LOW:
            return RISK_MEDIUM
        elif likelihood[1] == RISK_MEDIUM:
            return RISK_HIGH
        elif likelihood[1] == RISK_HIGH:
            return RISK_CRITICAL
        raise Exception("This should not happen!")
