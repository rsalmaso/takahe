from django.http import HttpRequest
from hatchway import ApiResponse, api_view

from activities.models import TimelineEvent
from activities.services import TimelineService
from api import schemas
from api.decorators import scope_required
from api.pagination import MastodonPaginator, PaginatingApiResponse, PaginationResult


@scope_required("read:notifications")
@api_view.get
def notifications(
    request: HttpRequest,
    max_id: str | None = None,
    since_id: str | None = None,
    min_id: str | None = None,
    limit: int = 20,
    account_id: str | None = None,
) -> ApiResponse[list[schemas.Notification]]:
    # Types/exclude_types use weird syntax so we have to handle them manually
    base_types = {
        "favourite": TimelineEvent.Types.liked,
        "reblog": TimelineEvent.Types.boosted,
        "mention": TimelineEvent.Types.mentioned,
        "follow": TimelineEvent.Types.followed,
        "admin.sign_up": TimelineEvent.Types.identity_created,
    }
    requested_types = set(request.GET.getlist("types[]"))
    excluded_types = set(request.GET.getlist("exclude_types[]"))
    if not requested_types:
        requested_types = set(base_types.keys())
    requested_types.difference_update(excluded_types)
    # Use that to pull relevant events
    queryset = TimelineService(request.identity).notifications(
        [base_types[r] for r in requested_types if r in base_types]
    )
    paginator = MastodonPaginator()
    pager: PaginationResult[TimelineEvent] = paginator.paginate(
        queryset,
        min_id=min_id,
        max_id=max_id,
        since_id=since_id,
        limit=limit,
    )
    return PaginatingApiResponse(
        [schemas.Notification.from_timeline_event(event) for event in pager.results],
        request=request,
        include_params=["limit", "account_id"],
    )
