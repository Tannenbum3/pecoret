from ddf import G
from backend.models.advisory import Advisory, Roles
from backend.models.advisory_membership import AdvisoryMembership
from .base import PeCoReTTestCaseMixin


class AdvisoryTestCaseMixin(PeCoReTTestCaseMixin):
    def init_mixin(self):
        super().init_mixin()
        self.vendor1 = self.create_user("testvendor1", "changeme1234", group="Vendor")
        self.read_only_vendor = self.create_user("readonlyvendor1", "changeme1234", group="Vendor")
        self.vendor2 = self.create_user("testvendor2", "changeme1234", group="Vendor")
        self.advisory1 = self.create_instance(Advisory, is_draft=False, user=self.pentester1)
        self.advisory2 = self.create_instance(Advisory, is_draft=True, user=self.pentester2)
        self.assign_advisory_role(self.vendor1, Roles.VENDOR, self.advisory1)
        self.assign_advisory_role(self.read_only_vendor, Roles.READ_ONLY, self.advisory1)

    def assign_advisory_role(self, user, role, advisory):
        return G(AdvisoryMembership, user=user, role=role, advisory=advisory)
