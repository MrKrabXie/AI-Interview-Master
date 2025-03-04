import sqlite3
# from langchain_ollama import Ollama
from langchain_ollama import OllamaEmbeddings, OllamaLLM  # 新的导入路径
from langchain_core.prompts import ChatPromptTemplate

# ========================
# 数据库配置
# ========================
DB_FILE = '../scraped_data.db'
SOURCE_TABLE = 'boss_interview_questions'

# ========================
# 核心业务逻辑
# ========================
def generate_enhanced_answer():
    """生成优化答案的主函数"""
    try:
        # 初始化模型
        llm = OllamaLLM(model="mistral",  temperature=0.7)
        # 创建处理链
        prompt_template = ChatPromptTemplate.from_template('''
            [角色] 资深技术面试官，需要优化候选人的回答。
            
            [原始问题] {question}
            [当前回答] {reference_answer}
            
            请执行：
            1. 技术术语准确性检查（√/×标注）
            2. 补充2023年行业最新实践案例
            3. 使用STAR(Situation、Task、Action、Result)法则重组回答结构
            4. 输出Markdown格式的优化版本
            ''')
        chain = prompt_template | llm

        # 获取并处理数据
        data = get_random_question_with_id()
        if not data:
            return "无法获取有效问题"

        # 生成优化答案
        ai_answer = chain.invoke(data)
        # ai_answer = optimized.str

        # 持久化存储
        save_to_ai_answers(
            question_id=data['id'],
            original_question=data['question'],
            reference_answer=data['reference_answer'],
            ai_answer=ai_answer
        )

        # 标记原记录
        mark_answered(data['id'])

        return ai_answer

    except Exception as e:
        print(f"处理失败: {str(e)}")
        return "服务暂时不可用，请稍后再试"

# ========================
# 数据库操作
# ========================
def get_random_question_with_id(db_file=DB_FILE):
    """获取带ID的随机问题"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute(f'''
            SELECT id, content, answer 
            FROM {SOURCE_TABLE}
            WHERE answer IS NOT NULL 
            AND (is_answer_by_ai IS NULL OR is_answer_by_ai = 0)
            ORDER BY RANDOM() 
            LIMIT 1
        ''')

        if row := cursor.fetchone():
            return {
                "id": row[0],
                "question": row[1],
                "reference_answer": row[2]
            }
        return None

    except sqlite3.Error as e:
        print(f"数据库错误: {str(e)}")
        return None
    finally:
        if conn: conn.close()

def save_to_ai_answers(question_id, original_question, reference_answer, ai_answer):
    """保存AI回答到数据库"""
    conn = sqlite3.connect(DB_FILE)
    try:
        # 建表（如果不存在）
        conn.execute('''
            CREATE TABLE IF NOT EXISTS ai_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_table TEXT NOT NULL DEFAULT 'boss_interview_questions',
                question_id INTEGER NOT NULL,
                original_question TEXT NOT NULL,
                reference_answer TEXT,
                ai_answer TEXT NOT NULL,
                generated_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(question_id) REFERENCES boss_interview_questions(id)
            )
        ''')

        # 插入记录
        conn.execute('''
            INSERT INTO ai_answers 
            (question_id, original_question, reference_answer, ai_answer)
            VALUES (?, ?, ?, ?)
        ''', (question_id, original_question, reference_answer, ai_answer))

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"数据存储失败: {str(e)}")
    finally:
        conn.close()

def mark_answered(question_id):
    """标记原问题为已处理"""
    conn = sqlite3.connect(DB_FILE)
    try:
        conn.execute(f'''
            UPDATE {SOURCE_TABLE} 
            SET is_answer_by_ai = 1 
            WHERE id = ?
        ''', (question_id,))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"状态更新失败: {str(e)}")
    finally:
        conn.close()

# 执行示例
if __name__ == "__main__":
    result = generate_enhanced_answer()
    print("优化后的回答：\n", result)
