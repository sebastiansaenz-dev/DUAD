const student = {
  name: "John Doe",
  grades: [
    { name: "math", grade: 80 },
    { name: "science", grade: 100 },
    { name: "history", grade: 60 },
    { name: "PE", grade: 90 },
    { name: "music", grade: 98 },
  ],
};

const studentSummary = (student) => {
  const average = () => {
    let sum = 0;
    for (const subject of student.grades) {
      sum += subject.grade;
    }

    const finalAverage = sum / student.grades.length;

    return finalAverage;
  };

  const highGrade = student.grades.reduce((max, current) => {
    return current.grade > max.grade ? current : max;
  });

  const lowGrade = student.grades.reduce((min, current) => {
    return current.grade < min.grade ? current : min;
  });

  return {
    name: student.name,
    gradeAvg: average(),
    highestGrade: highGrade.name,
    lowestGrade: lowGrade.name,
  };
};

console.log(studentSummary(student));
