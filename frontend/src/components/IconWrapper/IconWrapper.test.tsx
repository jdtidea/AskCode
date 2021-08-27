import {render} from 'test';
import {IconWrapper} from './IconWrapper';

describe(IconWrapper.name, () => {
  it('Should render', () => {
    const {getByText} = render(<IconWrapper>{<p>test</p>}</IconWrapper>);
    expect(getByText('test')).toBeTruthy();
  });
});
