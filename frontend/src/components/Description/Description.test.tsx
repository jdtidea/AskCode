import {render} from 'test';
import {Description} from './Description';

describe(Description.name, () => {
  it('Should render', () => {
    const {baseElement} = render(<Description />);
    expect(baseElement).toBeDefined();
  });
});
