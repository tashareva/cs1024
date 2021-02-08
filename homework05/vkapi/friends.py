import dataclasses
import math
import time
import typing as tp

from vkapi import session
from vkapi.config import VK_CONFIG
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    parameters = {
        "access_token": VK_CONFIG["access_token"],
        "v": VK_CONFIG["version"],
        "user_id": user_id if user_id is not None else " ",
        "count": count,
        "offset": offset,
        "fields": ",".join(fields) if fields is not None else " ",
    }
    response = session.get("friends.get", params=parameters)
    document = response.json()
    if "error" in document or not response.ok:
        raise APIError(document["error"]["error_msg"])
    else:
        return FriendsResponse(
            count=response.json()["response"]["count"], items=response.json()["response"]["items"]
        )


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    if target_uids is None:
        parameters = {
            "access_token": VK_CONFIG["access_token"],
            "v": VK_CONFIG["version"],
            "source_uid": source_uid if source_uid is not None else "",
            "target_uid": target_uid,
            "order": order,
        }
        response = session.get(f"friends.getMutual", params=parameters)
        response_json = response.json()
        if "error" in response_json or not response.ok:
            raise APIError(response_json["error"]["error_msg"])
        return response_json["response"]

    responses = []
    if progress is None:
        progress = lambda x: x
    for i in progress(range(((len(target_uids) + 99) // 100))):
        parameters = {
            "access_token": VK_CONFIG["access_token"],
            "v": VK_CONFIG["version"],
            "target_uids": ",".join(map(str, target_uids)),
            "order": order,
            "count": count if count is not None else "",
            "offset": offset + i * 100,
        }
        response = session.get(f"friends.getMutual", params=parameters)
        filee = response.json()
        if "error" in filee or not response.ok:
            raise APIError(filee["error"]["error_msg"])
        for arg in filee["response"]:
            responses.append(
                MutualFriends(
                    id=arg["id"],
                    common_friends=arg["common_friends"],
                    common_count=arg["common_count"],
                )
            )
        if i % 3 == 2:
            time.sleep(1)
    return responses
