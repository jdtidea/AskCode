import {render} from 'test';
import {Toast} from './Toast';

describe(Toast.name, () => {
  it('Should render', () => {
    const {getAllByText} = render(<Toast text={<p>Toast</p>} />);
    expect(getAllByText('Toast')).toBeTruthy();
  });
});
