import {render} from 'test';
import {AnswerSkill} from './AnswerSkill';

describe(AnswerSkill.name, () => {
  it('Should render', () => {
    const {baseElement} = render(<AnswerSkill onPress={() => {}} />);
    expect(baseElement).toBeDefined();
  });
});
