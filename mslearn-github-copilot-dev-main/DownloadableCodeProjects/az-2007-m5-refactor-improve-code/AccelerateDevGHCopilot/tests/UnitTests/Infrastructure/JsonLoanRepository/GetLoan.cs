using Library.ApplicationCore;
using Library.Infrastructure.Data;
using Library.ApplicationCore.Entities;
using Microsoft.Extensions.Configuration;
using NSubstitute;
using Xunit;

namespace UnitTests.Infrastructure.JsonLoanRepositoryTests
{
    public class GetLoan
    {
        private readonly ILoanRepository _mockLoanRepository;
        private readonly JsonLoanRepository _jsonLoanRepository;
        private readonly IConfiguration _configuration;
        private readonly JsonData _jsonData;

        public GetLoan()
        {
            _mockLoanRepository = Substitute.For<ILoanRepository>();
            _configuration = new ConfigurationBuilder().Build();
            _jsonData = new JsonData(_configuration);
            _jsonLoanRepository = new JsonLoanRepository(_jsonData);
        }

        [Fact(DisplayName = "JsonLoanRepository.GetLoan: Returns loan when ID is found")]
        public async Task GetLoan_ReturnsLoanWhenIdIsFound()
        {
            // Arrange
            var loanId = 1; // Loan ID that exists in Loans.json
            var expectedLoan = new Loan
            {
                Id = loanId,
                BookItemId = 17,
                PatronId = 22,
                LoanDate = DateTime.Parse("2023-12-08T00:40:43.1808862"),
                DueDate = DateTime.Parse("2023-12-22T00:40:43.1808862"),
                ReturnDate = null
            };

            _mockLoanRepository.GetLoan(loanId).Returns(expectedLoan);

            // Act
            var actualLoan = await _jsonLoanRepository.GetLoan(loanId);

            // Assert
            Assert.NotNull(actualLoan);
            Assert.Equal(expectedLoan.Id, actualLoan!.Id);
            Assert.Equal(expectedLoan.BookItemId, actualLoan.BookItemId);
            Assert.Equal(expectedLoan.PatronId, actualLoan.PatronId);
            Assert.Equal(expectedLoan.LoanDate, actualLoan.LoanDate);
            Assert.Equal(expectedLoan.DueDate, actualLoan.DueDate);
            Assert.Equal(expectedLoan.ReturnDate, actualLoan.ReturnDate);
        }

        [Fact(DisplayName = "JsonLoanRepository.GetLoan: Returns null when ID is not found")]
        public async Task GetLoan_ReturnsNullWhenIdIsNotFound()
        {
            // Arrange
            var loanId = 999; // Loan ID that does not exist in Loans.json

            _mockLoanRepository.GetLoan(loanId).Returns((Loan?)null);

            // Act
            var actualLoan = await _jsonLoanRepository.GetLoan(loanId);

            // Assert
            Assert.Null(actualLoan);
        }

        // Add more test methods here
    }
}