import datetime
import logging
import pickle
from typing import Any, Dict

from lightfm import LightFM
from pydantic import BaseModel, ConfigDict
from scipy.sparse import csr_matrix

logger = logging.getLogger(__name__)


class ProfileModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    user_id_map: Dict[str, int]
    item_id_map: Dict[str, int]
    item_feature_map: Dict[str, int]
    item_features_matrix: csr_matrix
    interactions: csr_matrix
    info: Dict[str, Any]
    model: LightFM

    @classmethod
    def load_from_pickle(cls, path):
        with open(f"{path}/model.pkl", "rb") as f:
            start = datetime.datetime.now()
            model = pickle.load(f)
            logger.info(
                f"Loaded model in {(datetime.datetime.now() - start).microseconds / 1000} milliseconds"
            )
        with open(f"{path}/interactions.pkl", "rb") as f:
            start = datetime.datetime.now()
            interactions = pickle.load(f)
            logger.info(
                f"Loaded interactions in {(datetime.datetime.now() - start).microseconds / 1000} milliseconds"
            )
        with open(f"{path}/item_features_matrix.pkl", "rb") as f:
            start = datetime.datetime.now()
            item_features_matrix = pickle.load(f)
            logger.info(
                f"Loaded item_features_matrix in {(datetime.datetime.now() - start).microseconds / 1000} milliseconds"
            )
        with open(f"{path}/model_info.pkl", "rb") as f:
            start = datetime.datetime.now()
            info = pickle.load(f)
            logger.info(
                f"Loaded model_train_date in {(datetime.datetime.now() - start).microseconds / 1000} milliseconds"
            )
        with open(f"{path}/dataset.pkl", "rb") as f:
            start = datetime.datetime.now()
            dataset = pickle.load(f)
            user_id_map, _, item_id_map, item_feature_map = dataset.mapping()
            logger.info(
                f"Loaded dataset in {(datetime.datetime.now() - start).microseconds / 1000} milliseconds"
            )
        return cls(
            model=model,
            interactions=interactions,
            info=info,
            user_id_map=user_id_map,
            item_id_map=item_id_map,
            item_feature_map=item_feature_map,
            item_features_matrix=item_features_matrix,
        )
