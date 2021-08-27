import {ChangeEvent, FormEvent, useCallback, useState} from 'react';
import {Card, Label, TextInput} from '@uitk/react';
import {Button} from '@uitk/react';
import {Search} from '@uitk/react-icons';
import './SearchCard.scss';

// TODO: Combine this component with SearchBar
interface ISearchCard {
  onSubmit: (value: string) => void;
}

export function SearchCard({onSubmit}: ISearchCard) {
  const [value, setValue] = useState<string>('');

  const changeHandler = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => {
      e.preventDefault();
      setValue(e.target.value);
    },
    [setValue],
  );

  const handleSubmit = useCallback(
    (e: FormEvent) => {
      e.preventDefault();
      onSubmit(value);
    },
    [value, onSubmit],
  );

  return (
    <div>
      <Card className="main-card">
        <div>
          <div className="label-holder">
            <Label className="how-label">How can we help?</Label>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="input-btn-container">
              <TextInput
                value={value}
                onChange={changeHandler}
                id="text-input"
                required
                autoFocus
              />
              <Button className="ask-btn" type="submit" icon={<Search />}>
                Ask Optum
              </Button>
            </div>
          </form>
        </div>
      </Card>
    </div>
  );
}
