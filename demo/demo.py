"""
面试宝典APP 代码结构设计 v1.3
增强了相似度计算、评分分级、答题反馈和奖励机制
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ======================
# 1. 数据采集系统
# ======================
class DataCollector:
    def __init__(self):
        self.crawlers = {
            'boss': BossSpider(),
            'leetcode': LeetcodeSpider(),
            'zhihu': ZhihuSpider()
        }

    def run_spider(self, platform):
        """执行指定平台的爬虫"""
        questions = self.crawlers[platform].fetch()
        cleaned_questions = self.clean_and_filter_questions(questions)
        return cleaned_questions

    def clean_and_filter_questions(self, questions):
        """去重、相似度计算，筛选出不重复的题目"""
        unique_questions = []
        existing_questions = []  # 已经存入数据库的题目
        for question in questions:
            if self.is_similar_to_existing(question, existing_questions):
                continue
            unique_questions.append(question)
            existing_questions.append(question)
        return unique_questions

    def is_similar_to_existing(self, question, existing_questions):
        """计算题目相似度，过滤掉相似度高的题目"""
        vectorizer = TfidfVectorizer()
        all_questions = existing_questions + [question]
        tfidf_matrix = vectorizer.fit_transform(all_questions)
        similarity_matrix = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
        max_similarity = np.max(similarity_matrix)
        return max_similarity > 0.8  # 如果相似度超过0.8，则认为是重复的

# ======================
# 2. 面试题评分和分级
# ======================
class QuestionScorer:
    def __init__(self):
        pass

    def grade_question(self, question):
        """根据题目内容和标签评分，1到5分"""
        difficulty = self.calculate_difficulty(question)
        score = self.calculate_score(question)
        return {
            'difficulty': difficulty,
            'score': score
        }

    def calculate_difficulty(self, question):
        """计算题目难度，基于内容和标签"""
        # 假设题目难度是通过关键词和标签的权重计算出来的
        keywords = question.get('tags', [])
        difficulty = sum([self.get_keyword_difficulty(tag) for tag in keywords]) / len(keywords)
        return min(max(difficulty, 1), 5)  # 保证难度在1到5之间

    def calculate_score(self, question):
        """计算题目评分，基于题目质量和用户反馈"""
        # 评分逻辑可以基于历史用户反馈
        score = 3  # 示例，实际应根据用户评价调整
        return min(max(score, 1), 5)

    def get_keyword_difficulty(self, keyword):
        """根据关键词返回对应的难度"""
        keyword_difficulty_map = {
            'java': 3,
            'big data': 4,
            'algorithm': 5,
            'basic': 2
        }
        return keyword_difficulty_map.get(keyword.lower(), 2)

# ======================
# 3. 答案学习与反馈
# ======================
class AnswerGenerator:
    def __init__(self):
        self.templates = {
            'algorithm': AlgorithmTemplate(),
            'system_design': STARTemplate(),
            'behavior': STARTemplate()
        }

    def generate(self, question_type, raw_data):
        """根据题目类型选择模板"""
        template = self.templates[question_type]
        return template.apply(
            content=raw_data,
            priority_builder=self._build_priority
        )

    def update_model(self, feedback_data):
        """通过用户反馈优化模型"""
        model_trainer = ModelTrainer()
        model_trainer.retrain_model(feedback_data)

# ======================
# 4. 面试题提问和回答机制
# ======================
class InterviewQuestion:
    def __init__(self):
        self.questions_asked = 0

    def ask_question(self, user_id, question):
        """提问接口，用户提问时获得积分"""
        points = self.calculate_points(question)
        self.award_points(user_id, points)
        self.questions_asked += 1
        return {"question": question, "points_awarded": points}

    def answer_question(self, user_id, question, answer):
        """回答接口，回答正确后获得积分"""
        points = self.calculate_points(question)
        self.award_points(user_id, points)
        # 保存答案到数据库
        self.save_answer_to_db(question, answer)
        return {"answer": answer, "points_awarded": points}

    def calculate_points(self, question):
        """根据题目评分计算积分"""
        score = question['score']
        difficulty = question['difficulty']
        return score * difficulty  # 积分为评分与难度的乘积

    def award_points(self, user_id, points):
        """根据用户行为给予积分"""
        # 假设我们有一个积分系统，这里简化为存储用户积分
        user = User.get(user_id)
        user.points += points
        user.save()

    def save_answer_to_db(self, question, answer):
        """保存用户答案到数据库"""
        db.save({
            'question_id': question['id'],
            'answer': answer
        })

# ======================
# 数据库设计
# ======================
"""
数据库设计要点：
1. 题目表(questions)
   - id, title, type(P0-P3), tags[], source, raw_content, difficulty, score

2. 答案表(answers)
   - id, question_id, answer_content, user_id

3. 用户表(users)
   - user_id, username, points

4. 用户反馈表(feedback)
   - user_id, question_id, feedback_content, rating
"""

# ======================
# 启动配置
# ======================
if __name__ == '__main__':
    collector = DataCollector().run_spider('boss')
    for question in collector:
        question_score = QuestionScorer().grade_question(question)
        print(f"Question: {question['title']}, Difficulty: {question_score['difficulty']}, Score: {question_score['score']}")

    # 示例提问和回答
    interview = InterviewQuestion()
    user_id = 1
    question = {"id": 123, "title": "Explain the difference between Java and C++", "score": 4, "difficulty": 3}
    answer = "Java is a high-level, interpreted language, while C++ is a compiled language..."

    response = interview.answer_question(user_id, question, answer)
    print(response)
