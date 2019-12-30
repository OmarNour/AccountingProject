from django.db import models
# from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from AccountingApp.models import Currencies, ExchangeRate
from AccountingApp.views import get_exchange_rate

User = get_user_model()
# Create your models here.


class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, default=User, on_delete=models.CASCADE, related_name='organization_owner')
    name = models.CharField(null=False, blank=False, max_length=255)
    email = models.EmailField(null=True, blank=True)
    # main_org = models.ForeignKey('self', null=True, blank=True, related_name='organization_main_org')

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=User, related_name='organization_created_by')
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='organization_modified_by')
    updated_date = models.DateTimeField(null= True, blank=True, editable=False)

    class Meta:
        unique_together = ('owner', 'name')

    def __str__(self):
        return '{}-{}'.format(self.id,self.name)

#
# class ActiveOrganizaition(models.Model):
#     organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     class Meta:
#         unique_together = ('organization', 'user')


class InvitedUsers(models.Model):
    # send url if email is new, if exist, then send a notification to login and accept joining the Organization
    # always insert record in OrganizationMember with user_accept=False
    inviter_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='inviter_users_user')
    invite_to_org = models.ForeignKey(Organization, on_delete=models.CASCADE, null=False, blank=False, related_name='invited_users_user_to_org')
    invited_user_first_name = models.CharField(max_length=100, null=False,blank=False)
    invited_user_last_name = models.CharField(max_length=100, null=False, blank=False)
    invited_user_email = models.EmailField(null=False,blank=False)

    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='invited_users_user')
    invited_date = models.DateTimeField(default=timezone.now, editable=False)

    invitation_url = models.URLField(null=False)
    invitation_sent = models.BooleanField(default=False)
    invitation_accepted_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('invite_to_org', 'invited_user_email')

    def __str__(self):
        return self.invited_user_email


class OrganizationMember(models.Model):
    # user_accept will be True if s/he created new Organization or signup from a an invitation link
    organization_id = models.ForeignKey(Organization,
                                        related_name="OrganizationMember_organization_id",
                                        on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='OrganizationMember_user')
    invitation_id = models.ForeignKey(InvitedUsers, on_delete=models.CASCADE, null=True, related_name='OrganizationMember_invitation_id')
    # user_accept = models.BooleanField(null=False, default=False)
    active = models.BooleanField(null=False,default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('organization_id', 'user')


class OrgCurrencies(models.Model):
    Org_id = models.ForeignKey(Organization, on_delete=models.CASCADE, null=False,blank=False, related_name='OrgCurrencies_org_id')
    currency_id = models.ForeignKey(Currencies, on_delete=models.CASCADE, null=False, blank=False, related_name='OrgCurrencies_currency_id')
    decimal_precision = models.IntegerField(default=2, null=False, blank=False)
    base_currency = models.BooleanField(default=False)

    """
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=User, related_name='OrgCurrencies_created_by')
    created_date = models.DateTimeField(default=timezone.now(), editable=False)

    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='OrgCurrencies_modified_by')
    updated_date = models.DateTimeField(null=True, blank=True, editable=False)
    """
    class Meta:
        unique_together = ('Org_id', 'currency_id')

    def __str__(self):
        return '{} {}'.format(self.currency_id, '(Base)' if self.base_currency else '')


class OrgExchangeRate(models.Model):
    Org_id = models.ForeignKey(Organization, on_delete=models.CASCADE, null=False, blank=False, related_name='OrgExchangeRate_Org_id')
    ex_rate_id = models.ForeignKey(ExchangeRate, on_delete=models.CASCADE,null=False, blank=False, related_name='OrgExchangeRate_ex_rate_id')
    related_OrgCurrencies = models.ForeignKey(OrgCurrencies, on_delete=models.CASCADE, related_name='OrgExchangeRate_related_curr_id')

    from_currency_id = models.ForeignKey(OrgCurrencies, on_delete=models.CASCADE, related_name='OrgExchangeRate_from_currency_id')
    to_currency_id = models.ForeignKey(OrgCurrencies, on_delete=models.CASCADE, related_name='OrgExchangeRate_to_currency_id')

    swapped_current_rate = models.DecimalField(max_digits=30, decimal_places=6, default=0, null=False, blank=False)
    override_rate = models.DecimalField(max_digits=30, decimal_places=6, default=0, null=False, blank=False)
    last_updated = models.DateTimeField(default=timezone.now, null=False, blank=False)

    """
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=User, related_name='OrgExchangeRate_created_by')
    created_date = models.DateTimeField(default=timezone.now(), editable=False)

    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='OrgExchangeRate_modified_by')
    updated_date = models.DateTimeField(null=True, blank=True, editable=False)
    """

    class Meta:
        unique_together = ('Org_id', 'related_OrgCurrencies')

    def __str__(self):
        return '{} To {}: {}'.format(self.from_currency_id,
                                     self.to_currency_id,
                                     self.override_rate if self.override_rate > 0 else get_exchange_rate(self.from_currency_id,
                                                                                                                       self.to_currency_id))

