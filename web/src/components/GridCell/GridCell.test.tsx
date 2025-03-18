import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import GridCell from './GridCell';
import { Grid } from '../../store/useGridStore';

import { describe } from '@jest/globals'

describe('GridCell', () => {  it('calls toggleCellState with correct arguments when clicked', () => {
    const mockToggleCellState = jest.fn();
    const mockSetShaking = jest.fn();
    const rowIndex = 2;
    const columnIndex = 3;
    const grid: Grid = {
      width: 4,
      height: 3,
      cells: [
        [
          {
            module: null,
            label: '',
            value: 0,
            type: '',
            total: 0.0,
            adjacency_bonus: 0.0,
            bonus: 0.0,
            active: true,
            adjacency: false,
            tech: null,
            supercharged: false,
            sc_eligible: false,
            image: null,
          },
          {
            module: null,
            label: '',
            value: 0,
            type: '',
            total: 0.0,
            adjacency_bonus: 0.0,
            bonus: 0.0,
            active: true,
            adjacency: false,
            tech: null,
            supercharged: false,
            sc_eligible: false,
            image: null,
          },
          {
            module: null,
            label: '',
            value: 0,
            type: '',
            total: 0.0,
            adjacency_bonus: 0.0,
            bonus: 0.0,
            active: true,
            adjacency: false,
            tech: null,
            supercharged: false,
            sc_eligible: false,
            image: null,
          },
          {
            module: null,
            label: '',
            value: 0,
            type: '',
            total: 0.0,
            adjacency_bonus: 0.0,
            bonus: 0.0,
            active: true,
            adjacency: false,
            tech: null,
            supercharged: false,
            sc_eligible: false,
            image: null,
          },
        ],
        [
          {
            module: null,
            label: '',
            value: 0,
            type: '',
            total: 0.0,
            adjacency_bonus: 0.0,
            bonus: 0.0,
            active: true,
            adjacency: false,
            tech: null,
            supercharged: false,
            sc_eligible: false,
            image: null,
          },
          {
            module: null,
            label: '',
            value: 0,
            type: '',
            total: 0.0,
            adjacency_bonus: 0.0,
            bonus: 0.0,
            active: true,
            adjacency: false,
            tech: null,
            supercharged: false,
            sc_eligible: false,
            image: null,
          },
          {
            module: null,
            label: '',
            value: 0,
            type: '',
            total: 0.0,
            adjacency_bonus: 0.0,
            bonus: 0.0,
            active: true,
            adjacency: false,
            tech: null,
            supercharged: false,
            sc_eligible: false,
            image: null,
          },
          {
            module: null,
            label: '',
            value: 0,
            type: '',
            total: 0.0,
            adjacency_bonus: 0.0,
            bonus: 0.0,
            active: true,
            adjacency: false,
            tech: null,
            supercharged: false,
            sc_eligible: false,
            image: null,
          },
        ],
        [
          {
            module: null,
            label: '',
            value: 0,
            type: '',
            total: 0.0,
            adjacency_bonus: 0.0,
            bonus: 0.0,
            active: true,
            adjacency: false,
            tech: null,
            supercharged: false,
            sc_eligible: false,
            image: null,
          },
          {
            module: null,
            label: '',
            value: 0,
            type: '',
            total: 0.0,
            adjacency_bonus: 0.0,
            bonus: 0.0,
            active: true,
            adjacency: false,
            tech: null,
            supercharged: false,
            sc_eligible: false,
            image: null,
          },
          {
            module: null,
            label: '',
            value: 0,
            type: '',
            total: 0.0,
            adjacency_bonus: 0.0,
            bonus: 0.0,
            active: true,
            adjacency: false,
            tech: null,
            supercharged: false,
            sc_eligible: false,
            image: null,
          },
          {
            module: null,
            label: '',
            value: 0,
            type: '',
            total: 0.0,
            adjacency_bonus: 0.0,
            bonus: 0.0,
            active: true,
            adjacency: false,
            tech: null,
            supercharged: false,
            sc_eligible: false,
            image: null,
          },
        ],
      ],
    };

    render(
      <GridCell
        rowIndex={rowIndex}
        columnIndex={columnIndex}
        cell={{}}
        grid={grid}
        toggleCellState={mockToggleCellState}
        setShaking={mockSetShaking}
      />
    );

    const cellElement = screen.getByRole('gridCell');
    fireEvent.click(cellElement);

    expect(mockToggleCellState).toHaveBeenCalledWith(rowIndex, columnIndex, expect.any(Object));
  });});
