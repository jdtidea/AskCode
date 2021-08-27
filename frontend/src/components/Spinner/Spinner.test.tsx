import {render} from 'test';
import {Spinner} from './Spinner';

describe(Spinner.name, () => {
  it('Should render', () => {
    const {baseElement} = render(<Spinner />);
    expect(baseElement).toBeDefined();
  });
});
