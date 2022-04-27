// import  sum  from './Function'
const sum = require('./Function')
test('验证2加4是否等于6', ()=>{
    expect(sum(2, 4)).toBe(6);
});
// test('验证6减2是否等于4',()=>{
//     expect(sub(6, 2)).toBe(4);
// });
test('null',()=>{
    const n = null;
    expect(n).toBeNull();
    expect(n).toBeDefined();
    expect(n).not.toBeUndefined();
    expect(n).not.toBeTruthy();
    expect(n).toBeFalsy();
});

test('两个浮点数相加',()=>{
    // expect(sum(0.1, 0.2)).toBe(0.3);
    expect(sum(0.1, 0.2)).toBeCloseTo(0.3);
});