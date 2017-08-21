from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, default=User, related_name='organization_owner')
    name = models.CharField(null=False, blank=False, max_length=255)
    email = models.EmailField(null=True, blank=True)
    main_org = models.ForeignKey('self', null=True, blank=True, related_name='organization_main_org')

    created_by = models.ForeignKey(User, default=User, related_name='organization_created_by')
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    modified_by = models.ForeignKey(User, null=True, blank=True, related_name='organization_modified_by')
    updated_date = models.DateTimeField(null= True, blank=True, editable=False)

    class Meta:
        unique_together = ('owner', 'name')

    def get_absolute_url(self):
        return reverse("organizations:detail", kwargs={'pk': self.pk})

    def __str__(self):
        return '{}-{}'.format(self.id,self.name)


class OrganizationMember(models.Model):
    organization_id = models.ForeignKey(Organization,
                                        related_name="OrganizationMember_organization_id",
                                        on_delete=models.PROTECT)
    user = models.ForeignKey(User,related_name='OrganizationMember_user')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('organization_id', 'user')
