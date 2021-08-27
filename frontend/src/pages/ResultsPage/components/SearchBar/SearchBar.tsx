import {ChangeEvent, FormEvent} from 'react';
import styled from 'styled-components';
import {FormControl, Label, TextInput} from '@uitk/react';
import {Button} from 'components';
import {Grid} from 'layout';

interface ISearchBar {
  onSubmit: (e: FormEvent) => void;
  value?: string;
  onChange: (e: ChangeEvent<HTMLInputElement>) => void;
}
const Wrapper = styled(Grid)`
  text-align: left;
  align-items: flex-end;
  max-width: 100%;
  box-shadow: 0px 10px 5px 0px rgba(204, 204, 204, 1);
`;

export function SearchBar({onSubmit, onChange, value}: ISearchBar) {
  return (
    <Wrapper>
      <form onSubmit={onSubmit}>
        <div className="row" style={{alignItems: 'flex-end'}}>
          <div className="col-s-12 col-m-1 col-l-2"></div>
          <div className="col-s-12 col-m-7 col-l-6">
            <FormControl id="search">
              <Label>How can we help?</Label>
              <TextInput
                value={value}
                onChange={onChange}
                className="text-input"
              />
            </FormControl>
          </div>
          <div className="col-s-12 col-m-3 col-l-2">
            <Button.Search />
          </div>
          <div className="col-s-12 col-m-1 col-l-2"></div>
        </div>
      </form>
    </Wrapper>
  );
}
