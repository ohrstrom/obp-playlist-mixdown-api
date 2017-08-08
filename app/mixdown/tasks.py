from __future__ import absolute_import

import logging

from celery import shared_task
from django.core.files import File

from .remote import APIClient
from .renderer import Renderer

log = logging.getLogger(__name__)


@shared_task
def render_playlist_task(obj):

    log.debug('Render playlist {}'.format(obj.pk))

    r = Renderer()

    obj._skip_content_hash_check = True

    try:

        mixdown_path = r.render(playlist_id=obj.pk, playlist_uri=obj.remote_uri)

        with open(mixdown_path, 'rb') as f:
            mixdown_file = File(f)
            obj.status = obj.STATUS_DONE

            obj.mixdown_file.save('mixdown.mp3', mixdown_file, False)

        log.info('successfully rendered playlist id: {}'.format(obj.pk))


    except Exception as e:

        log.error('error rendering playlist id: {} - {}'.format(obj.pk, e))
        obj.status = obj.STATUS_ERROR

    # cleans all renderer artefacts
    r.cleanup()

    obj.task_id = None
    obj.save()

    # inform remote api
    url = '{}{}'.format(obj.remote_uri, 'mixdown-complete/')
    r = APIClient().post(url, data=[])

    print(r.status_code)
