from process_question import process_question

if __name__ == '__main__':
    with open("questions.txt", "r") as r_fi:
        total = 0.0
        correct = 0.0
        while True:
            question = r_fi.readline()
            answer = r_fi.readline()
            if not answer:
                break  # EOF
            answer = answer.lower().rstrip()
            watson_answer_set = process_question(question)
            print("Watson Answer Set: ", watson_answer_set)
            print("Answer: ", answer)
            # Not None
            if watson_answer_set:
                for ans in watson_answer_set:
                    watson_answer = ans.lower()
                    if watson_answer == answer or answer in watson_answer:
                        print("Match is found!")
                        correct += 1.0
                        break
            total += 1.0
        print("Num Correct: " , correct)
        print("Total Num: " , total)
        print("Accuracy Score: ", (correct / total))
