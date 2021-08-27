import {render} from 'test';
import {Markdown} from './Markdown';

describe(Markdown.name, () => {
  it('Should render', () => {
    const {getByText} = render(<Markdown content="# Test" />);
    expect(getByText('Test')).toBeTruthy();
  });
});
