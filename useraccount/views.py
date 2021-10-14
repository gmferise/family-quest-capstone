from website.base_views import BaseEndpoint
from useraccount.models import UserAccount
from familystructure.models import Person
from django.db.models import Q, F, Value
from django.db.models.functions import Concat, Lower

class UserSearchEndpoint(BaseEndpoint):

    def get(self, request):
        """Search for users by name or email"""
        search = request.GET.get('q', None)
        if search is None:
            return self.not_ok()
        
        search_terms = ''.join(
            char for char in search
            if ( ord(char) >= 48 and ord(char) <= 122 )
            or char == ' '
        ).split(' ')

        if len(search_terms) == 1:
            search_regex = search_terms[0]
        else:
            search_regex = '[a-z ]*'.join(f'{s}[a-z]*' for s in search_terms)

        users = (
            UserAccount.objects
            .filter(Q(person__isnull=True) & Q(email__icontains=search))
        )
        people = (
            Person.objects
                .filter(is_claimed=True)
                .select_related('useraccount')
                .annotate(
                    name=Concat(
                        Lower(F('first_name')), Value(' '),
                        Lower(F('nickname')), Value(' '),
                        Lower(F('middle_name')), Value(' '),
                        Lower(F('last_name')), Value(' '),
                        Lower(F('title')),
                    ),
                    email=F('useraccount__email'),
                )
                .filter(Q(name__iregex=search_regex) | Q(email__icontains=search))
        )
        return self.ok(request, { 'useraccounts': ([{
                'id': person.useraccount.id,
                'email': person.useraccount.email,
                'name': str(person),
            } for person in people] + [{
                'id': user.id,
                'email': user.email,
                'name': '',
            } for user in users])[:5]
        })