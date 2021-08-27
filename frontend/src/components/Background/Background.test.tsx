import {render} from 'test';
import {Background} from './Background';

describe(Background.name, () => {
  it('Should render', () => {
    const {baseElement} = render(
      <Background fullImage="https://image.com/image.png" />,
    );
    expect(baseElement).toBeDefined();
  });
});
