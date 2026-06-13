from django.urls import reverse


def text_is_present(value):
    return bool((value or '').strip())


def has_basic_profile(user):
    return all([
        bool(user.username) and user.username != user.email,
        bool(user.gender),
        bool(user.role),
    ])

def get_onboarding_step(user):
    if not user.is_authenticated:
        return None
    if not has_basic_profile(user):
        return 'onboarding_basic'
    if user.is_employer:
        if not has_employer_profile(user):
            return 'onboarding_employer'
        return None
    if not has_job_seeker_profile(user):
        return 'onboarding_job_seeker'
    return None


def get_employer_profile(user):
    return getattr(user, 'employer_profile', None)


def has_employer_profile(user):
    profile = get_employer_profile(user)
    if profile is None:
        return False
    return all([
        text_is_present(profile.company_name),
        text_is_present(profile.industry),
        text_is_present(profile.location),
        text_is_present(profile.description),
        text_is_present(profile.position),
    ])


def has_job_seeker_profile(user):
    return user.onboarding_complete





def get_onboarding_redirect_url(user):
    step = get_onboarding_step(user)
    if step is None:
        return None
    return reverse(step)


def get_authenticated_home_url(user):
    onboarding_url = get_onboarding_redirect_url(user)
    if onboarding_url:
        return onboarding_url
    if user.is_employer:
        return reverse('employers_index')
    return reverse('index')
