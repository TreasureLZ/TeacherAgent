import os
import uuid
from django.conf import settings


def get_upload_path(instance, filename):
    """
    生成规范化的上传路径：
    media/data/{应用标签}/{模型名称}/{UUID文件名}
    """
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{ext}"

    return os.path.join(
        settings.UPLOAD_PATH_TEMPLATE.format(
            app_label=instance._meta.app_label,
            model_name=instance._meta.model_name
        ),
        new_filename
    )