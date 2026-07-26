from ...models.media_models import MediaCompletion, MediaStatus
from .authors_data import INOUE_TAKHEHIKO, KISHIMOTO_MASASHI
from .categories_data import (
    ACTION_GENRE,
    ADVENTURE_GENRE,
    AWARD_WINNING_GENRE,
    FANTASY_GENRE,
    MARTIAL_ARTS_THEME,
    SCHOOL_THEME,
    SHOUNEN_DEMOGRAPHIC,
    SPORTS_GENRE,
    TEAM_SPORTS_THEME,
)

SLAM_DUNK_MANGA = {
    "mal_id": 51,
    "title": "Slam Dunk",
    "small_image_url": "https://cdn.myanimelist.net/images/manga/2/258749t.webp",
    "image_url": "https://cdn.myanimelist.net/images/manga/2/258749.webp",
    "large_image_url": "https://cdn.myanimelist.net/images/manga/2/258749l.webp",
    "format": "Manga",
    "synopsis": 'Hanamichi Sakuragi, a tall, boisterous teenager with flame-red hair and physical strength beyond his years, is eager to put an end to his rejection streak of 50 and finally score a girlfriend as he begins his first year of Shohoku High. However, his reputation for delinquency and destructiveness precedes him, and most of his fellow students subsequently avoid him like the plague. As his first day of school ends, he is left with two strong thoughts: "I hate basketball" and "I need a girlfriend."\n\nHaruko Akagi, ignorant of Hanamichi\'s history of misbehavior, notices his immense height and unwittingly approaches him, asking whether or not he likes basketball. Overcome by the fact that a girl is speaking to him, the red-haired giant blurts out a yes despite his true feelings. At the gym, Haruko asks if he can do a slam dunk. Though a complete novice, Hanamachi palms the ball and makes the leap...but overshoots, slamming his head into the backboard. Amazed by his near-inhuman physical abilities, Haruko quickly notifies the school\'s basketball captain of his feat. With this, Hanamichi is unexpectedly thrust into a world of competition for a girl he barely knows, but he soon discovers that there is perhaps more to basketball than he once thought.',
    "score": 9.09,
    "rank": 7,
    "status": MediaStatus.FINISHED,
    "themes": [SCHOOL_THEME, TEAM_SPORTS_THEME],
    "genres": [
        AWARD_WINNING_GENRE,
        SPORTS_GENRE,
    ],
    "demographics": [SHOUNEN_DEMOGRAPHIC],
    "number_sections": 31,
    "chapters": 276,
    "authors": [INOUE_TAKHEHIKO],
    "user_score": None,
    "user_completion": MediaCompletion.NOT_STARTED,
    "user_current_section": 0,
}

NARUTO_MANGA = {
    "mal_id": 11,
    "title": "Naruto",
    "small_image_url": "https://cdn.myanimelist.net/images/manga/3/249658t.webp",
    "image_url": "https://cdn.myanimelist.net/images/manga/3/249658.webp",
    "large_image_url": "https://cdn.myanimelist.net/images/manga/3/249658l.webp",
    "format": "Manga",
    "synopsis": "Whenever Naruto Uzumaki proclaims that he will someday become the Hokage—a title bestowed upon the best ninja in the Village Hidden in the Leaves—no one takes him seriously. Since birth, Naruto has been shunned and ridiculed by his fellow villagers. But their contempt isn't because Naruto is loud-mouthed, mischievous, or because of his ineptitude in the ninja arts, but because there is a demon inside him. Prior to Naruto's birth, the powerful and deadly Nine-Tailed Fox attacked the village. In order to stop the rampage, the Fourth Hokage sacrificed his life to seal the demon inside the body of the newborn Naruto.\n\nAnd so when he is assigned to Team 7—along with his new teammates Sasuke Uchiha and Sakura Haruno, under the mentorship of veteran ninja Kakashi Hatake—Naruto is forced to work together with other people for the first time in his life. Through undergoing vigorous training and taking on challenging missions, Naruto must learn what it means to work in a team and carve his own route toward becoming a full-fledged ninja recognized by his village.",
    "score": 8.08,
    "rank": 698,
    "status": MediaStatus.FINISHED,
    "themes": [MARTIAL_ARTS_THEME],
    "genres": [
        ACTION_GENRE,
        ADVENTURE_GENRE,
        FANTASY_GENRE,
    ],
    "demographics": [SHOUNEN_DEMOGRAPHIC],
    "number_sections": 72,
    "chapters": 700,
    "authors": [KISHIMOTO_MASASHI],
    "user_score": 7,
    "user_completion": MediaCompletion.IN_PROGRESS,
    "user_current_section": 71,
}
