from question_types.translation.qn_builder import begin_exercise as translation_exercise
from question_types.fill_blank_qns.qn_builder import begin_exercise as fill_blank_exercise
from question_types.vocab_qns.qn_builder import begin_exercise as vocab_exercise


def main():
    while True:
        print('\n--- Pensa Latina ---')
        print('1: Vocabulary')
        print('2: Translation (Latin → English)')
        print('3: Translation (English → Latin)')
        print('4: Fill in the blank')
        print('e: Exit')

        choice = input('\nChoose an exercise: ').strip().lower()

        if choice == '1':
            print('\nVocabulary mode:')
            print('1: Latin → English')
            print('2: English → Latin')
            print('3: Both')
            mode_choice = input('Choose mode: ').strip()
            mode_map = {'1': 'latin', '2': 'english', '3': 'both'}
            mode = mode_map.get(mode_choice, 'latin')
            vocab_exercise(mode=mode)
        elif choice == '2':
            translation_exercise(from_english=False)
        elif choice == '3':
            translation_exercise(from_english=True)
        elif choice == '4':
            fill_blank_exercise()
        elif choice == 'e':
            print('Vale!')
            break
        else:
            print('Unrecognized input. Try again.')


if __name__ == '__main__':
    main()
