using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc.ModelBinding.Validation;

namespace MVC2.Models
{
    public class Employee
    { 
		public string FullName { get; set; }
        [ValidateNever]
        public string VideoUrl { get; set; }
        [ValidateNever]
        public string ImageUrl { get; set; }


    }
}