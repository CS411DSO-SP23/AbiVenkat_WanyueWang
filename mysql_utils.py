import pymysql
import pandas as pd

# Note: the password needs to be 'password'
db = pymysql.connect(host='localhost',
                user='root',
                password='password',
                database='academicworld',
                charset='utf8mb4',
                port=3306,
                cursorclass=pymysql.cursors.DictCursor)


def get_top_universities(keyword):
    results_df = pd.DataFrame(columns=["University", "Faculty Count", "Faculty Name", "Score"])

    with db.cursor() as cursor:
        # Find the top 5 universities for the given keyword
        top_universities_sql = """
                        SELECT
                            U.id AS university_id,
                            U.name AS university_name,
                            COUNT(DISTINCT F.id) AS faculty_count
                        FROM
                            university U
                            JOIN faculty F ON F.university_id = U.id
                            JOIN faculty_keyword FK ON FK.faculty_id = F.id
                            JOIN keyword K ON K.id = FK.keyword_id
                        WHERE
                            K.name = %s
                        GROUP BY
                            U.id,
                            U.name
                        ORDER BY
                            faculty_count DESC,
                            U.name
                        LIMIT 5;
                        """

        cursor.execute(top_universities_sql, (keyword,))
        top_universities = cursor.fetchall()

        for university in top_universities:
            university_id = university['university_id']
            university_name = university['university_name']
            faculty_count = university['faculty_count']
            # print(f"University: {university_name}, Faculty Count: {faculty_count}")

            # Append the data as a new row to the DataFrame
            new_row = pd.DataFrame({
                "University": [university_name],
                "Faculty Count": [faculty_count],
                "Faculty Name": "",
                "Score": ""
            })

            results_df = pd.concat([results_df, new_row], ignore_index=True)

            # Find the top 5 faculty members for each university with the keyword
            top_faculty_sql = """
                                SELECT
                                    F.id AS faculty_id,
                                    F.name AS faculty_name,
                                    FK.score
                                FROM
                                    faculty F
                                    JOIN faculty_keyword FK ON FK.faculty_id = F.id
                                    JOIN keyword K ON K.id = FK.keyword_id
                                WHERE
                                    F.university_id = %s
                                    AND K.name = %s
                                ORDER BY
                                    FK.score DESC,
                                    F.name
                                LIMIT 5;
                                """

            cursor.execute(top_faculty_sql, (university_id, keyword))
            top_faculty = cursor.fetchall()

            for faculty in top_faculty:
                faculty_id = faculty['faculty_id']
                faculty_name = faculty['faculty_name']
                score = faculty['score']
                # print(f"  Faculty: {faculty_name}, Score: {score}")

                # Append the data as a new row to the DataFrame
                new_row = pd.DataFrame({
                    "University": "",
                    "Faculty Count": "",
                    "Faculty Name": [faculty_name],
                    "Score": [score]
                })

                results_df = pd.concat([results_df, new_row], ignore_index=True)

    return results_df


def get_coauthored_count(faculty_name, university_name, start_year, end_year):
    with db.cursor() as cursor:
        # Find the number of co-authored paper for the given faculty during the given time range
        top_universities_sql = """
                                SELECT
                                    F.name,
                                    COUNT(DISTINCT P.id) AS coauthored_papers
                                FROM
                                    faculty F
                                    JOIN university U ON U.id = F.university_id
                                    JOIN faculty_publication FP ON F.id = FP.faculty_id
                                    JOIN publication P ON P.id = FP.publication_id
                                    JOIN faculty_publication FP2 ON P.id = FP2.publication_id
                                    JOIN faculty F2 ON F2.id = FP2.faculty_id
                                WHERE
                                    F.name = %s
                                    AND U.name = %s
                                    AND F2.name != %s
                                    AND P.year BETWEEN %s AND %s
                                GROUP BY
                                    F.name;

                                """

        cursor.execute(top_universities_sql, (faculty_name, university_name, faculty_name, start_year, end_year))
        coauthored_count = cursor.fetchall()

    return coauthored_count

# print(get_coauthored_count("Antonio Torralba", "Massachusetts Institute of Technology", '0', '2023'))

