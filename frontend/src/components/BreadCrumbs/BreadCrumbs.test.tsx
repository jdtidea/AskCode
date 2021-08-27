import {render} from 'test';
import {BreadCrumbs} from './BreadCrumbs';

describe(BreadCrumbs.name, () => {
  it('Should render', () => {
    const {baseElement} = render(<BreadCrumbs />);
    expect(baseElement).toBeTruthy();
  });
});
