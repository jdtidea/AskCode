import {render} from 'test';
import {Banner} from './Banner';

describe(Banner.name, () => {
  it('Should render', () => {
    const {baseElement} = render(<Banner />);
    expect(baseElement).toBeDefined();
  });
});
