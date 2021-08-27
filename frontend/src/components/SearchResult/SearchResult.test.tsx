import {render} from 'test';
import {SearchResult, ISearchResult} from './SearchResult';
import {Domains} from 'types';

const defaultProps: ISearchResult = {
  query: 'back pain',
  index: 1,
  title: 'title',
  url: '',
  skill: 'AVA',
  domain: Domains.benefits,
  content: 'test',
  variant: 'md',
  score: 0,
};
describe(SearchResult.name, () => {
  it('Should render', () => {
    const {getByText} = render(<SearchResult {...defaultProps} />);
    expect(getByText('test')).toBeTruthy();
  });
});
